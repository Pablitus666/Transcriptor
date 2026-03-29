# 📝 Transcriptor V1.0

**Sistema de transcripción automática de audios con aceleración por GPU**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![WhisperX](https://img.shields.io/badge/Motor-WhisperX-black)
![CUDA](https://img.shields.io/badge/GPU-NVIDIA%20CUDA%2012.1-76B900)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6)
![Build](https://img.shields.io/badge/build-beta-orange)
![Version](https://img.shields.io/badge/version-1.0.0-blueviolet)

---

## 📌 Descripción general

**Transcriptor V1.0** es una aplicación de escritorio desarrollada en **Python** para la **transcripción de audios**. Utiliza el motor **WhisperX** con alineación fonética y un sistema de **Lógica Gramatical de Turnos**, optimizado para el contexto de entrevistas en **Bolivia**.

El sistema aprovecha la **GPU (NVIDIA CUDA)** para reducir los tiempos de procesamiento y genera documentos en formato Word con identificación de oradores.

---

![Social Preview](images/Preview.png)

---

## 🎯 Características principales

* Interfaz gráfica basada en **Tkinter** compatible con pantallas **HiDPI**.
* Motor **WhisperX** con alineación fonética (sincronía a nivel de palabra).
* **Aceleración por hardware**: Soporte nativo para **NVIDIA CUDA 12.1**.
* **Lógica Gramatical de Turnos**: Sistema de reasignación automática que identifica el patrón "Pregunta-Respuesta" para corregir errores de diarización.
* **Fusión de oradores**: Algoritmo que unifica segmentos consecutivos del mismo hablante para evitar etiquetas duplicadas.
* **Diccionario Nacional**: Integración de nombres de calles de Tarija y una base de datos de **934 nombres y apellidos** comunes en toda Bolivia para una capitalización y ortografía correcta.
* **Motor RunMatcher**: Manipulación de XML interno de Word para aplicar negritas y subrayados en los encabezados de orador sin alterar la fuente Arial 11.
* **Soporte Multi-idioma**: Interfaz con detección automática para 9 idiomas.
* Procesamiento asíncrono en segundo plano para mantener la estabilidad de la interfaz.

---

## 🖥 Interfaz de usuario

La aplicación cuenta con:

* Selección de carpeta de audios y opcionalmente plantilla DOCX.
* Selector de modelo (small, medium, large-v3).
* **Selector de Género Profesional**: Define si la etiqueta del entrevistador es "Psicólogo" o "Psicóloga".
* Barra de progreso y consola de eventos en tiempo real.
* Sistema portable que no requiere acceso al registro de Windows.

---

## 📷 Capturas de pantalla

<p align="center">
  <img src="images/screenshot.png?v=2" alt="Vista previa de la aplicación" width="600"/>
</p>

---

## ⚙️ Arquitectura del sistema

```
Transcripciones/
│
├─ gui/                # Ventanas y componentes de la interfaz
├─ core/               # Lógica de orquestación, post-procesamiento e i18n
├─ utils/              # Diccionario OSM, léxico y utilidades
├─ exporters/          # Motor de exportación DOCX
├─ assets/             # Imágenes, fuentes y archivos de traducción
├─ whisper_env/        # Entorno virtual con soporte CUDA
├─ models_cache/       # Modelos de IA descargados
└─ main.py             # Punto de entrada
```

---

## 📦 Requisitos técnicos

* Windows 10 / 11 (64-bit)
* Python 3.11
* GPU NVIDIA compatible con CUDA (Recomendado para velocidad)

Dependencias principales:
* `whisperx`
* `torch` (CUDA 12.1)
* `pyannote.audio`
* `python-docx`

---

## 🏛 Enfoque del proyecto

* **Estructura lógica**: Basada en la dinámica real de entrevistas en Cámara Gesell.
* **Privacidad**: Procesamiento local sin envío de datos a la nube.
* **Precisión**: Uso de léxico institucional y geográfico de Tarija.

---

## 📄 Licencia

Uso restringido a fines institucionales o internos. La redistribución requiere autorización del autor.

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**  
Software Developer

📍 Tarija, Bolivia <img src="https://flagcdn.com/w20/bo.png" width="20"/> <br>
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com) 

© 2026 — Transcriptor

--- 

## ⭐ Estado del proyecto

✔ En desarrollo (Fase Beta)
✔ Motor de GPU funcional
✔ Lógica gramatical activa
