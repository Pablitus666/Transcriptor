from PIL import Image, ImageTk
import os
from typing import Optional, Tuple
from collections import OrderedDict
from core.image_enhancer import add_shadow, add_relief

class ImageManager:
    """ Gestiona carga, escalado y efectos (DPI + Relieve + Sombra) - Réplica de Wordy. """

    def __init__(self, root, max_cache_size: int = 32):
        self.root = root
        self._photo_cache = OrderedDict()
        self._pil_cache = OrderedDict()
        self.max_cache_size = max_cache_size
        
        try:
            # Detección de escalado DPI
            self.scale = root.winfo_fpixels('1i') / 96.0
        except Exception:
            self.scale = 1.0

    def load(
        self,
        filepath: str,
        size: Optional[Tuple[int, int]] = None,
        add_shadow_effect: bool = False,
        add_relief_effect: bool = False,
        relief_intensity: int = 2,
        shadow_offset: Tuple[int, int] = (3, 3),
        shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 90),
        blur_radius: int = 3,
        border: int = 5
    ) -> ImageTk.PhotoImage:
        
        cache_key = (filepath, size, add_shadow_effect, add_relief_effect, relief_intensity, self.scale)
        
        if cache_key in self._photo_cache:
            self._photo_cache.move_to_end(cache_key)
            return self._photo_cache[cache_key]

        try:
            pil_image = self._get_base_pil(filepath)

            # 1. Redimensionar considerando el escalado DPI (Directo y Estable)
            if size:
                physical_w = int(size[0] * self.scale)
                physical_h = int(size[1] * self.scale)
                pil_image = pil_image.resize((physical_w, physical_h), Image.LANCZOS)

            # 2. Aplicar Relieve si se solicita
            if add_relief_effect:
                pil_image = add_relief(pil_image, intensity=relief_intensity)

            # 3. Aplicar Sombra si se solicita
            if add_shadow_effect:
                pil_image = add_shadow(
                    pil_image, 
                    offset=shadow_offset, 
                    shadow_color=shadow_color,
                    blur_radius=blur_radius,
                    border=border
                )

            tk_img = ImageTk.PhotoImage(pil_image)
            self._store_in_cache(cache_key, tk_img)
            return tk_img
            
        except Exception as e:
            print(f"❌ Error cargando {filepath}: {e}")
            return None

    def _store_in_cache(self, key, value):
        self._photo_cache[key] = value
        if len(self._photo_cache) > self.max_cache_size:
            self._photo_cache.popitem(last=False)

    def _get_base_pil(self, filepath: str) -> Image.Image:
        if filepath in self._pil_cache:
            self._pil_cache.move_to_end(filepath)
            return self._pil_cache[filepath]

        if os.path.exists(filepath):
            with Image.open(filepath) as img:
                pil_img = img.convert("RGBA")
                self._pil_cache[filepath] = pil_img
                if len(self._pil_cache) > self.max_cache_size:
                    self._pil_cache.popitem(last=False)
                return pil_img
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
