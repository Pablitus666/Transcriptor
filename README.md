# 📝 Transcriptor V1.0

**Sistema de transcripción automática con inteligencia gramatical y aceleración por GPU**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![WhisperX](https://img.shields.io/badge/Motor-WhisperX-black)
![CUDA](https://img.shields.io/badge/GPU-NVIDIA%20CUDA-76B900)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6)
![Build](https://img.shields.io/badge/build-beta-orange)
![Version](https://img.shields.io/badge/version-1.0.0-blueviolet)

---

## 📌 Descripción general

**Transcriptor V1.0** es una solución desarrollada en **Python** para la **transcripción automatizada**. Integra el motor **WhisperX** con alineación fonética y una **Lógica Gramatical de Turnos**, diseñada para entrevistas en **Cámara Gesell** y entornos institucionales en **Bolivia**.

El sistema utiliza la potencia de la **GPU (NVIDIA CUDA)** para procesar audios extensos en segundos, garantizando una estructura documental idéntica a la transcripción manual profesional.

---

![Social Preview](images/Preview.png)

---

## 🎯 Características Principales (Nivel Élite)

* **Motor WhisperX V30+**: Integración de alineación fonética para una sincronía de palabras de ±30ms.
* **Aceleración por GPU**: Optimizado para **NVIDIA CUDA 12.1**, permitiendo el uso del modelo `large-v3` a máxima velocidad.
* **Lógica Gramatical de Turnos (V40)**: Cerebro artificial que entiende la dinámica "Pregunta-Respuesta", corrigiendo automáticamente errores de diarización cuando la IA de voz confunde a los oradores.
* **Fusión Atómica**: Algoritmo que garantiza la eliminación total de duplicados de etiquetas (Psicóloga/Víctima), logrando un flujo de lectura limpio y profesional.
* **Diccionario de Tarija (OSM)**: Base de datos integrada con **1,120 nombres de calles, avenidas y barrios** de Tarija, Bolivia, extraídos de OpenStreetMap para una capitalización perfecta.
* **Motor RunMatcher**: Manipulación quirúrgica del XML de Word para aplicar negritas y subrayados institucionales (Arial 11) sin dañar el formato original.
* **Protección de Tablas**: El sistema identifica y protege las tablas de cabecera, manteniendo intactos los datos de Fiscales y Víctimas.
* **Soporte Multi-idioma (i18n)**: Interfaz global en **9 idiomas** con detección automática del sistema operativo.

---

## ⚙️ Arquitectura del Sistema

```
Transcripciones/
│
├─ gui/                # Interfaz gráfica institucional (HiDPI)
├─ core/               # Motores V40 (Orquestador, Post-procesamiento, i18n)
├─ utils/              # Diccionario Tarija (OSM), léxico institucional
├─ exporters/          # Motor RunMatcher y exportación DOCX Quirúrgica
├─ models_cache/       # Modelos IA locales (Whisper, Pyannote, Wav2Vec2)
├─ whisper_env/        # Entorno virtual con soporte CUDA 12.1
├─ output/             # Destino de documentos institucionales
└─ main.py             # Punto de entrada de la aplicación
```

---

## 🚀 Ejecución del Sistema

La aplicación está diseñada para la portabilidad total:

1. **iniciar.vbs**: Ejecución invisible que verifica el entorno, componentes de GPU y crea el acceso directo en el escritorio.
2. **ejecutar.bat**: Lanzador directo del entorno virtual optimizado.

---

## 📦 Requisitos Técnicos

* **SO**: Windows 10 / 11 (64-bit).
* **Hardware**: Tarjeta de Video NVIDIA (Recomendado para velocidad Élite).
* **Entorno**: Contenido íntegramente en la carpeta `whisper_env`.

---

## 🏛 Enfoque Institucional

Este proyecto redefine la precisión documental en Bolivia:

* **Fidelidad Forense**: Respeta silencios, pausas reflexivas y turnos gramaticales.
* **Contexto Local**: Optimizado para el léxico de la FELCV, SLIM y el Ministerio Público.
* **Privacidad Total**: Procesamiento 100% offline (una vez descargados los modelos).

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**  
Software Developer

📍 Tarija, Bolivia <img src="https://flagcdn.com/w20/bo.png" width="20"/> <br>
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com) 

© 2026 — Transcriptor Élite

--- 

## ⭐ Estado del proyecto

✔ Nivel Forense Alcanzado
✔ Producción Estable
✔ Optimización por GPU Activa
