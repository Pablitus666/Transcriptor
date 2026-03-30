# 🚀 Transcriptor — Notas de Versión 1.0

---

## ✨ Versión 1.0.0 (Base Tecnológica)

Esta versión inicial establece la arquitectura base del sistema, centrada en la integración de motores de reconocimiento de voz de alta precisión y lógica aplicada al diálogo judicial.

---

## 🎯 Mejoras Técnicas Implementadas

### 🧠 Motor de Lógica Gramatical
Se ha desarrollado un sistema de control de turnos que analiza la estructura gramatical de la conversación.
* **Funcionamiento**: Detecta signos de interrogación para anticipar cambios de orador, corrigiendo automáticamente la asignación de respuestas de la víctima que el motor de voz pudiera confundir.

### ⚛️ Fusión Atómica de Segmentos
Implementación de un algoritmo de consolidación que unifica textos del mismo hablante.
* **Efecto**: Elimina la redundancia de etiquetas en el documento final, generando un flujo de lectura continuo y estructurado.

### 🏎️ Integración de WhisperX y CUDA
Migración al motor WhisperX con soporte para aceleración por hardware.
* **Rendimiento**: Optimización para NVIDIA CUDA 12.1, permitiendo el procesamiento de audios en una fracción del tiempo original mediante el uso de la GPU.

### 📍 Diccionario Nacional de Bolivia
Integración de una base de datos expandida para la normalización de texto.
* **Datos**: 934 nombres y apellidos comunes en Bolivia y 1,120 nombres de calles de Tarija.
* **Aplicación**: Asegura la ortografía y capitalización correcta de nombres propios y direcciones en todo el territorio nacional.

### ⚡ Optimización de Rendimiento
* **Búsqueda O(1)**: Implementación de mapas de léxico para una consulta instantánea del vocabulario, garantizando fluidez sin importar el tamaño de los diccionarios.

### 🖋️ Manejo Quirúrgico de XML (DOCX)
Uso del motor RunMatcher para la edición de archivos Word.
* **Precisión**: Permite aplicar formatos de resaltado sin alterar las propiedades de la fuente Arial 11 ni corromper la estructura de las tablas institucionales.

### 📁 Interfaz de Usuario Dinámica (Drag & Drop)
Implementación de soporte para el arrastre de archivos desde el explorador de Windows.
* **Productividad**: El usuario puede arrastrar una carpeta o un archivo de audio directamente al campo de entrada, eliminando la necesidad de navegar manualmente por los directorios.
* **Lógica Inteligente**: Si se arrastra un archivo individual, el sistema selecciona automáticamente la carpeta contenedora para iniciar la búsqueda de audios.

---

## 🏗️ Arquitectura y Estabilidad

* **Procesamiento Asíncrono**: Uso de multiprocessing para evitar bloqueos en la interfaz gráfica.
* **Internacionalización**: Soporte técnico para 9 idiomas con detección automática de locale.
* **Seguridad de Datos**: Eliminación de la salida TXT para concentrar la integridad del proceso en el formato DOCX institucional.

---

## 👨‍💻 Créditos

* **Desarrollo:** Walter Pablo Téllez Ayala
* **Tecnología:** WhisperX + Grammatical Engine
* **Versión:** 1.0.0 (Marzo 2026)

---

> *Transcriptor V1.0 combina procesamiento por hardware con reglas lingüísticas para automatizar la generación de actas y entrevistas con precisión técnica.*
