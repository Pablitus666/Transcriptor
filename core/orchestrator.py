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
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def _log(self, msg: str):
        if self.queue:
            self.queue(('log', msg))

    def _update_progress(self, val: float):
        if self.queue:
            self.queue(val)

    def scan_folder(self, folder_path: str) -> list:
        """Busca audios compatibles en la carpeta."""
        extensions = (".wav", ".mp3", ".flac", ".m4a")
        return [f for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

    def get_unprocessed_files(self, all_files: list) -> list:
        """Filtra archivos que ya tienen su .docx generado."""
        processed = {
            os.path.splitext(f)[0].replace('_transcrito', '').lower().strip()
            for f in os.listdir(self.output_dir)
            if f.lower().endswith('_transcrito.docx')
        }
        return [
            f for f in all_files 
            if os.path.splitext(f)[0].lower().strip() not in processed
        ]

    def process_all(self, folder: str, template: str, model_name: str, hf_token: str, prof_gender: str):
        """
        V1.0: Pipeline por Lotes (Batch Model Processing).
        Optimiza la velocidad cargando cada modelo una sola vez para todos los audios.
        Maneja la carga de audio bajo demanda para ahorrar RAM.
        """
        all_audios = self.scan_folder(folder)
        if not all_audios:
            if self.queue: self.queue(('done', "No se encontraron audios compatibles."))
            return

        to_process = self.get_unprocessed_files(all_audios)
        if not to_process:
            if self.queue: self.queue(('done', "✅ ¡Todos los audios ya han sido transcritos!"))
            return

        total_files = len(to_process)
        self._log(f"🚀 Iniciando Pipeline V1.0 para {total_files} archivos.")
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Diccionario para almacenar resultados intermedios de cada archivo
        results_map = {f: {"path": os.path.join(folder, f)} for f in to_process}

        try:
            # --- ETAPA 1: TRANSCRIPCIÓN (WhisperX) ---
            self._log(f"🧠 Cargando Motor de Transcripción ({model_name})...")
            whisper_model = models.cargar_whisper(model_name)
            
            for i, filename in enumerate(to_process, start=1):
                self._log(f"🎙 [{i}/{total_files}] Transcribiendo: {filename}")
                self._update_progress((i / total_files) * 30)
                audio = whisperx.load_audio(results_map[filename]["path"])
                # V1.0: Reducimos batch_size a 4 para estabilidad total en GPUs de consumo
                results_map[filename]["transcription"] = whisper_model.transcribe(audio, batch_size=4, language="es")
                del audio # Liberar RAM inmediatamente
                models.liberar_gpu() # Limpieza preventiva tras cada archivo
            
            del whisper_model
            models.liberar_gpu()
            self._log("✅ Transcripción base finalizada. Liberando GPU...")

            # --- ETAPA 2: ALINEACIÓN FONÉTICA (Wav2Vec2) ---
            self._log("🧠 Cargando Motor de Alineación Fonética...")
            align_model, align_metadata = models.cargar_modelo_alineacion("es")
            
            for i, filename in enumerate(to_process, start=1):
                self._log(f"📏 [{i}/{total_files}] Sincronizando palabras: {filename}")
                self._update_progress(30 + (i / total_files) * 20)
                
                audio = whisperx.load_audio(results_map[filename]["path"])
                segments = results_map[filename]["transcription"]["segments"]
                aligned = whisperx.align(segments, align_model, align_metadata, audio, device, return_char_alignments=False)
                results_map[filename]["aligned"] = aligned
                del audio # Liberar RAM
            
            del align_model
            models.liberar_gpu()
            self._log("✅ Alineación finalizada. Liberando GPU...")

            # --- ETAPA 3: DIARIZACIÓN (Pyannote) ---
            self._log("🧠 Cargando Motor de Diarización...")
            diar_pipeline = models.cargar_diarizacion(hf_token)
            
            for i, filename in enumerate(to_process, start=1):
                self._log(f"👥 [{i}/{total_files}] Identificando voces: {filename}")
                self._update_progress(50 + (i / total_files) * 25)
                
                audio_path = results_map[filename]["path"]
                results_map[filename]["diarization"] = diar_pipeline(audio_path, min_speakers=2, max_speakers=2)
            
            del diar_pipeline
            models.liberar_gpu()
            self._log("✅ Diarización finalizada. Liberando GPU...")

            # --- ETAPA 4: ASIGNACIÓN Y EXPORTACIÓN ---
            self._log("🖋 Generando documentos finales...")
            for i, filename in enumerate(to_process, start=1):
                self._log(f"📄 Exportando: {filename}")
                self._update_progress(75 + (i / total_files) * 25)
                
                base_name = os.path.splitext(filename)[0]
                res = results_map[filename]
                
                # Asignación word-level
                result_assigned = whisperx.assign_word_speakers(res["diarization"], res["aligned"])
                assigned = asignar_texto_v1(result_assigned["segments"])
                
                # Identificación Profesional (Inteligente V1.0)
                prof_id = identificar_psicologa(assigned)
                
                # Mapeo y Refinamiento
                labeled = []
                for s in assigned:
                    speaker_label = prof_gender if s["speaker_raw"] == prof_id else "Víctima"
                    labeled.append({
                        "speaker": speaker_label,
                        "text": s["text"],
                        "start": s.get("start", 0),
                        "end": s.get("end", 0)
                    })

                # Pipeline de post-procesado consolidado
                smoothed = suavizar_hablantes(labeled, umbral_breve=1.0)
                refined = refinar_turnos(smoothed, prof_gender)
                final_segments = fusionar(refined)

                # Exportación
                docx_path = os.path.join(self.output_dir, f"{base_name}_transcrito.docx")
                export_to_docx(final_segments, docx_path, template)
                
            self._log(f"🎊 ¡Pipeline Élite V1.0 finalizado con éxito! ({total_files} archivos)")

        except Exception as e:
            self._log(f"❌ Error crítico en el Pipeline: {str(e)}")
            models.liberar_gpu()

        if self.queue:
            self.queue(('done', f"✅ Transcripción completada exitosamente."))
