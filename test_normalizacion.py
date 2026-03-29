from utils.text import normalizar_texto

# === TEST DE ESTRÉS: TRILOGÍA DE LÉXICO FORENSE ===

texto_sucio = (
    "bueno estamos en la fel se ve de tarija con la psicóloga alejandra condori "
    "y el fiscal rodrigo vargas para la entrevista de la victima en la avenida victor paz "
    "cerca del puente san martin y el slim de la zona de villa abaroa [ruido] "
    "ya que el idif y la dna deben presentar el informe del caso zutara"
)

print("-" * 50)
print("ENTRADA CRUDA (Whisper):")
print(texto_sucio)
print("-" * 50)

resultado = normalizar_texto(texto_sucio)

print("RESULTADO PROCESADO (Motor Élite):")
print(resultado)
print("-" * 50)
