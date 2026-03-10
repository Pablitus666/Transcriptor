import os
import gc
import torch
from typing import Callable, Optional

from core.models import cargar_modelos
from core.transcription import transcribir, asignar_texto
from core.postprocess import identificar_psicologa, fusionar
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
        self._log("⏳ Cargando modelos...")
        whisper_model, diar_pipeline = cargar_modelos(model_name, hf_token)
        self._update_progress(5)
        self._log("✅ Modelos cargados correctamente\n")

        total = len(to_process)
        for idx, filename in enumerate(to_process, start=1):
            audio_path = os.path.join(folder, filename)
            base_name = os.path.splitext(filename)[0]
            prog_base = (idx - 1) / total * 100

            self._log(f"🎙 Procesando {filename} ({idx}/{total})...")

            # 2. Transcripción
            self._log("   - Transcribiendo...")
            segments_w = transcribir(audio_path, whisper_model, idioma="es")
            self._update_progress(prog_base + (100 / total) * 0.4)

            # 3. Diarización
            self._log("   - Diarizando...")
            diarization = diar_pipeline(audio_path)
            self._update_progress(prog_base + (100 / total) * 0.6)

            # 4. Post-proceso
            self._log("   - Asignando hablantes...")
            assigned = asignar_texto(segments_w, diarization)
            prof_id = identificar_psicologa(assigned)
            
            labeled = [
                {
                    "speaker": prof_gender if s["speaker_raw"] == prof_id else "Víctima", 
                    "text": s["text"]
                } 
                for s in assigned
            ]
            final_segments = fusionar(labeled)
            self._update_progress(prog_base + (100 / total) * 0.8)

            # 5. Exportación
            docx_path = os.path.join(self.output_dir, f"{base_name}_transcrito.docx")
            self._log("   - Generando DOCX profesional...")
            export_to_docx(final_segments, docx_path, template)
            
            self._update_progress(prog_base + (100 / total))
            self._log(f"✅ DOCX generado: {filename}\n")

            # 6. Limpieza de memoria
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        if self.queue:
            self.queue(('done', f"✅ ¡Transcripción completada! Se procesaron {total} archivos."))
