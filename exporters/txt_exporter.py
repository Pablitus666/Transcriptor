# exporters/txt_exporter.py
def guardar_txt(segmentos, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        for s in segmentos:
            f.write(f"{s['speaker']}: {s['text']}\n\n")
