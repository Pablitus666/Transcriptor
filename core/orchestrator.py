import os
import gc
import torch
import whisperx
from typing import Callable, Optional

from core import models
from core.transcription import asignar_texto_v1
from core.postprocess import identificar_psicologa, fusionar, refinar_turnos, suavizar_hablantes
from exporters.docx_exporter import export_to_docx

class TranscriptorOrchestrator:
    """
    Motor central de la aplicación. Orquesta la transcripción,
    diarización y exportación de múltiples audios.
    V1.0: Optimización por lotes y eficiencia de RAM.
    """
    def __init__(self, queue_callback: Optional[Callable] = None):
        self.queue = queue_callback

    def _log(self, msg: str):
        if self.queue:
            self.queue(('log', msg))

    def _update_progress(self, val: float):
        if self.queue:
            self.queue(val)

    def scan_folder(self, folder_path: str) -> list:
        """Busca audios compatibles en la carpeta."""
        extensions = (".wav", ".mp3", ".flac", ".m4a")
        try:
            return [f for f in os.listdir(folder_path) if f.lower().endswith(extensions)]
        except Exception as e:
            self._log(f"✖ Error al acceder a la carpeta: {str(e)}")
            return []

    def get_unprocessed_files(self, folder_path: str, all_files: list) -> list:
        """Filtra archivos que ya tienen su .docx generado en la misma carpeta."""
        processed = set()
        try:
            for f in os.listdir(folder_path):
                if f.lower().startswith('entrevista informativa_') and f.lower().endswith('.docx'):
                    # Extraemos el nombre base del audio del nombre del docx
                    name_part = f[23:-5] # Quita 'ENTREVISTA INFORMATIVA_' (23 chars) y '.docx' (5 chars)
                    processed.add(name_part.lower().strip())
        except: pass

        to_process = []
        for f in all_files:
            base_name = os.path.splitext(f)[0].lower().strip()
            if base_name not in processed:
                to_process.append(f)
        
        return to_process

    def process_all(self, folder: str, template: str, model_name: str, hf_token: str, prof_gender: str):        
        """
        V1.0: Pipeline por Lotes (Batch Model Processing).
        """
        all_audios = self.scan_folder(folder)
        if not all_audios:
            self._log("✖ No se encontraron archivos de audio (.wav, .mp3, .m4a, .flac) en la carpeta.")
            if self.queue: self.queue(('done', "No se encontraron audios compatibles."))
            return

        to_process = self.get_unprocessed_files(folder, all_audios)
        
        # LOG INFORMATIVO DE ELITE
        self._log(f"📦 Archivos encontrados: {len(all_audios)}")
        if len(to_process) < len(all_audios):
            skipped = len(all_audios) - len(to_process)
            self._log(f"✅ Se omitieron {skipped} audios que ya fueron procesados anteriormente.")

        if not to_process:
            self._log("✅ ¡Todos los audios de esta carpeta ya tienen su documento .docx!")
            if self.queue: self.queue(('done', "✅ Proceso finalizado (todo al día)."))
            return

        total_files = len(to_process)
        self._log(f"🚀 Iniciando Pipeline V1.0 para {total_files} archivos nuevos.")
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Diccionario para almacenar resultados intermedios
        results_map = {f: {"path": os.path.join(folder, f)} for f in to_process}

        try:
            # --- ETAPA 1: TRANSCRIPCIÓN (WhisperX) ---
            self._log(f"🧠 Cargando Motor de Transcripción ({model_name})...")
            whisper_model = models.cargar_whisper(model_name)

            for i, filename in enumerate(to_process, start=1):
                self._log(f"🎙 [1/1] Transcribiendo: {filename}")
                self._update_progress((i / total_files) * 30)
                audio = whisperx.load_audio(results_map[filename]["path"])
                results_map[filename]["transcription"] = whisper_model.transcribe(audio, batch_size=4, language="es")
                del audio
                models.liberar_gpu()

            del whisper_model
            models.liberar_gpu()

            # --- ETAPA 2: ALINEACIÓN FONÉTICA (Wav2Vec2) ---
            self._log("🧠 Cargando Motor de Alineación Fonética...")
            align_model, align_metadata = models.cargar_modelo_alineacion("es")

            for i, filename in enumerate(to_process, start=1):
                self._log(f"📑 [{i}/{total_files}] Sincronizando palabras: {filename}")
                self._update_progress(30 + (i / total_files) * 20)

                audio = whisperx.load_audio(results_map[filename]["path"])
                segments = results_map[filename]["transcription"]["segments"]
                aligned = whisperx.align(segments, align_model, align_metadata, audio, device, return_char_alignments=False)
                results_map[filename]["aligned"] = aligned
                del audio
                models.liberar_gpu()

            del align_model
            models.liberar_gpu()

            # --- ETAPA 3: DIARIZACIÓN (Pyannote) ---
            self._log("🧠 Cargando Motor de Diarización...")
            diar_pipeline = models.cargar_diarizacion(hf_token)

            for i, filename in enumerate(to_process, start=1):
                self._log(f"👥 [{i}/{total_files}] Identificando voces: {filename}")
                self._update_progress(50 + (i / total_files) * 25)

                audio_path = results_map[filename]["path"]
                results_map[filename]["diarization"] = diar_pipeline(audio_path, min_speakers=2, max_speakers=2)
                models.liberar_gpu()

            del diar_pipeline
            models.liberar_gpu()

            # --- ETAPA 4: ASIGNACIÓN Y EXPORTACIÓN ---
            self._log("✍ Generando documentos finales...")
            for i, filename in enumerate(to_process, start=1):
                self._log(f"📄 Exportando: {filename}")
                self._update_progress(75 + (i / total_files) * 25)

                base_name = os.path.splitext(filename)[0]
                res = results_map[filename]

                result_assigned = whisperx.assign_word_speakers(res["diarization"], res["aligned"])
                assigned = asignar_texto_v1(result_assigned["segments"])
                prof_id = identificar_psicologa(assigned)

                labeled = []
                for s in assigned:
                    speaker_label = prof_gender if s["speaker_raw"] == prof_id else "Víctima"
                    labeled.append({
                        "speaker": speaker_label, "text": s["text"],
                        "start": s.get("start", 0), "end": s.get("end", 0)
                    })

                final_segments = fusionar(refinar_turnos(suavizar_hablantes(labeled, umbral_breve=1.0), prof_gender))

                docx_filename = f"ENTREVISTA INFORMATIVA_{base_name}.docx"
                docx_path = os.path.join(folder, docx_filename)
                export_to_docx(final_segments, docx_path, template)

            self._log(f"🎊 ¡Proceso completado exitosamente! ({total_files} archivos)")

        except Exception as e:
            self._log(f"✖ Error crítico en el Pipeline: {str(e)}")
            models.liberar_gpu()

        if self.queue:
            self.queue(('done', f"✅ Transcripción completada exitosamente."))
