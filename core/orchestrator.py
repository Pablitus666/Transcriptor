import os
import gc
import torch
import whisperx
from typing import Callable, Optional

from core.models import cargar_modelos, cargar_modelo_alineacion
from core.transcription import transcribir_v30, asignar_texto_v30
from core.postprocess import identificar_psicologa, fusionar, refinar_turnos, limpiar_alucinaciones, suavizar_hablantes
from exporters.docx_exporter import export_to_docx

class TranscriptorOrchestrator:
    """
    Motor central de la aplicación. Orquesta la transcripción, 
    diarización y exportación de múltiples audios.
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
        Ejecuta el pipeline completo para todos los audios en la carpeta.
        """
        all_audios = self.scan_folder(folder)
        if not all_audios:
            if self.queue: self.queue(('done', "No se encontraron audios compatibles."))
            return

        to_process = self.get_unprocessed_files(all_audios)
        if not to_process:
            if self.queue: self.queue(('done', "✅ ¡Todos los audios ya han sido transcritos!"))
            return

        self._log(f"🔎 Mapeo finalizado. {len(to_process)} de {len(all_audios)} audios serán procesados.")

        # 1. Cargar modelos
        self._log("⏳ Cargando motores de inteligencia (V30)...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        whisper_model, diar_pipeline = cargar_modelos(model_name, hf_token)
        
        # Cargar motor de alineación fonética (Wav2Vec2)
        self._log("   - Sincronizando alineación fonética (Español)...")
        align_model, align_metadata = cargar_modelo_alineacion("es", device)
        
        self._update_progress(5)
        self._log("✅ Motores V30 listos para nivel forense\n")

        total = len(to_process)
        for idx, filename in enumerate(to_process, start=1):
            audio_path = os.path.join(folder, filename)
            base_name = os.path.splitext(filename)[0]
            prog_base = (idx - 1) / total * 100

            self._log(f"🎙 Procesando {filename} ({idx}/{total})...")

            try:
                # 2. Transcripción y Alineación Quirúrgica (V32 - Sincronía Fina)
                self._log("   - Transcribiendo audio (Motor WhisperX)...")
                audio = whisperx.load_audio(audio_path)

                result = whisper_model.transcribe(
                    audio, 
                    batch_size=16, 
                    language="es"
                )
                self._update_progress(prog_base + (100 / total) * 0.3)

                self._log("   - Sincronizando palabras (Alineación Fonética)...")
                result = whisperx.align(result["segments"], align_model, align_metadata, audio, device, return_char_alignments=False)
                self._update_progress(prog_base + (100 / total) * 0.5)

                self._log("   - Identificando voces (Diarización de Precisión)...")
                diar_segments = diar_pipeline(audio_path, min_speakers=2, max_speakers=2)
                self._update_progress(prog_base + (100 / total) * 0.7)

                self._log("   - Asignando turnos y normalizando texto...")
                result = whisperx.assign_word_speakers(diar_segments, result)
                assigned = asignar_texto_v30(result["segments"])
                self._update_progress(prog_base + (100 / total) * 0.8)
                
                # Identificación automática del profesional (Psicólogo/a)
                prof_id = identificar_psicologa(assigned)
                
                # Mapeo final de etiquetas institucionales y Limpieza de Alucinaciones
                labeled = []
                for s in assigned:
                    speaker_label = prof_gender if s["speaker_raw"] == prof_id else "Víctima"
                    
                    # Limpieza quirúrgica de alucinaciones (V31+)
                    texto_limpio = limpiar_alucinaciones(s["text"])
                    
                    labeled.append({
                        "speaker": speaker_label,
                        "text": texto_limpio,
                        "start": s.get("start", 0),
                        "end": s.get("end", 0)
                    })

                # Refinamiento Élite: Suavizar parpadeos y detectar preguntas fusionadas
                smoothed = suavizar_hablantes(labeled, umbral_breve=1.0)
                refined = refinar_turnos(smoothed, prof_gender)

                # Fusión final de segmentos con límite de silencio de equilibrio (V34: 1.3s)
                final_segments = fusionar(refined, max_silencio=1.3)
                self._update_progress(prog_base + (100 / total) * 0.8)

                # 4. Exportación Profesional DOCX
                docx_path = os.path.join(self.output_dir, f"{base_name}_transcrito.docx")
                self._log("   - Generando DOCX institucional (Arial 11)...")
                export_to_docx(final_segments, docx_path, template)
                
                self._update_progress(prog_base + (100 / total))
                self._log(f"✅ DOCX V32 generado con éxito: {filename}\n")

            except Exception as e:
                self._log(f"❌ Error procesando {filename}: {str(e)}")
                continue

            # 5. Limpieza agresiva de memoria para eficiencia industrial
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        if self.queue:
            self.queue(('done', f"✅ ¡Transcripción completada! Se procesaron {total} archivos."))
