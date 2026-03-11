# 📝 Transcriptor

**Sistema de transcripción automática de audios con interfaz gráfica profesional**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black)
![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6)
![Build](https://img.shields.io/badge/build-stable-brightgreen)
![License](https://img.shields.io/badge/license-Private%20Institutional-red)
![Version](https://img.shields.io/badge/version-1.0.0-blueviolet)

---

## 📌 Descripción general

**Transcriptor** es una aplicación de escritorio desarrollada en **Python** que permite la **transcripción automática de audios en español**, integrando modelos avanzados de **OpenAI Whisper** y diarización de hablantes, con una **interfaz gráfica moderna, estable y orientada a uso institucional**.

El sistema está diseñado para entornos donde se requiere **precisión, trazabilidad y facilidad de uso**, como entrevistas informativas, declaraciones, informes psicológicos y documentación administrativa.

---

![Social Preview](images/Preview.png)

---

## 🎯 Características principales

* Interfaz gráfica basada en **Tkinter**
* Transcripción automática mediante **Whisper (small, medium, large-v3)**
* Procesamiento en **segundo plano (multiprocessing)**
* Barra de progreso en tiempo real
* Registro detallado del proceso (log interno)
* Soporte para **plantillas DOCX personalizadas**
* **Motor de Búsqueda Quirúrgica "RunMatcher"**: Tecnología de nivel Élite que manipula el XML interno de Word para aplicar formatos sin romper estilos, imágenes o fuentes (Arial 11).
* **Inteligencia Lingüística Avanzada**: Identificación y resaltado automático (Negrita + Subrayado) de hablantes (**Psicólogo/a**, **Víctima**), ignorando tildes, mayúsculas, género y manejando límites de palabra complejos.
* **Soporte Multi-idioma (i18n)**: Interfaz global con detección automática del idioma del sistema operativo. Soporta **9 idiomas** (Español, Inglés, Alemán, Francés, Italiano, Japonés, Portugués, Ruso y Chino) con sistema de fallback inteligente.
* Diseño visual institucional (colores, iconografía, efectos HiDPI)
* Bloqueo inteligente de controles durante la ejecución
* Ventanas de diálogo personalizadas (StyledDialog)
* Sistema portable (no requiere instalación tradicional)

---

## 🖥 Interfaz de usuario

La aplicación cuenta con:

* Selección de carpeta de audios
* Selección opcional de plantilla DOCX
* Selección del modelo Whisper
* **Selector de Género Profesional**: Permite definir si quien entrevista es "Psicólogo" o "Psicóloga" para una personalización total del documento.
* Botones de acción con retroalimentación visual
* Barra de progreso dinámica
* Consola interna de eventos
* Ventana “Acerca de” integrada
* Control seguro de cierre durante procesos activos

La interfaz está optimizada para pantallas **HiDPI**, con renderizado mejorado de imágenes, sombras y relieve visual.

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
├─ gui/                # Interfaz gráfica (ventanas, widgets, diálogos)
├─ core/               # Lógica de transcripción, orquestación e i18n
├─ utils/              # Utilidades de texto, tiempo y recursos
├─ exporters/          # Motor RunMatcher y exportación DOCX
├─ assets/             # Recursos institucionales (imágenes, fuentes, locales)
├─ whisper_env/        # Entorno virtual aislado
├─ worker.py           # Proceso de transcripción (multiprocessing)
└─ main.py             # Punto de entrada de la aplicación
```

---

## 🔐 Seguridad y control de ejecución

El sistema incluye mecanismos para:

* Evitar ejecuciones simultáneas
* Bloquear botones durante la transcripción (bloqueo lógico, no visual)
* Confirmar cierre si hay procesos activos
* Validar existencia de archivos críticos
* Detectar movimientos indebidos de la carpeta base
* Mantener portabilidad sin uso del registro de Windows

---

## 🚀 Ejecución del sistema

El usuario final **no necesita interactuar con la consola**.

La aplicación se inicia mediante:

* Acceso directo creado automáticamente (con icono de alta resolución)
* Ejecución directa de `main.py` (vía entorno virtual) o binario compilado.

---

## 📦 Requisitos técnicos

* Windows 10 / 11
* Python 3.10+
* GPU opcional (CUDA recomendado para modelos grandes)

Dependencias principales:

* `faster-whisper`
* `torch`
* `pyannote.audio`
* `python-docx`
* `Pillow`

> Todas las dependencias se encuentran contenidas dentro del entorno virtual `whisper_env`.

---

## 🧾 Formatos de salida

* **DOCX PROFESIONAL** → Documento de alta fidelidad con hablantes resaltados quirúrgicamente y formato institucional Arial 11. (Se ha optimizado el flujo eliminando el formato TXT para centrarse en la excelencia documental).

---

## 🏛 Enfoque institucional

Este proyecto fue diseñado con criterios de:

* **Precisión Documental**: Resaltado automático de actores clave en el proceso psicológico/judicial.
* **Usabilidad**: Para personal no técnico.
* **Estabilidad operativa**: Gestión robusta de memoria y hilos.
* **Presentación profesional**: Documentos listos para archivo oficial.

---

## 📄 Licencia

---

### Licencia privada / institucional

Uso restringido a fines **internos o institucionales**.
La redistribución, modificación o comercialización requiere autorización expresa del autor.

---

## 👨‍💻 Autor

**Walter Pablo Téllez Ayala**  
Software Developer

📍 Tarija, Bolivia <img src="https://flagcdn.com/w20/bo.png" width="20"/> <br>
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com) 

© 2026 — QR - Generator

--- 

## ⭐ Estado del proyecto

✔ Estable
✔ En producción
✔ Orientado a uso profesional

---

⭐ Si este proyecto te resulta útil, considera dejar una estrella en el repositorio.