# 🚀 Transcriptor — Release Notes (Élite)

---

## ✨ Versión 2.0.0 — *The Surgical Update*

Esta versión representa un salto cualitativo en la arquitectura de la aplicación, integrando motores de procesamiento de texto de nivel avanzado y optimizando la salida documental para cumplir con los más altos estándares institucionales.

---

## 🎯 Novedades Destacadas

### 🖋️ Motor de Búsqueda Quirúrgica "RunMatcher"
Se ha integrado el motor de manipulación XML de nivel Élite. A diferencia de los métodos convencionales que pueden corromper el formato de Word, **RunMatcher** mapea y divide los "Runs" internos del archivo `.docx` de forma quirúrgica.
* **Beneficio**: Permite aplicar negritas y subrayados a palabras específicas sin alterar la fuente (Arial 11), el espaciado o las imágenes del documento institucional.

### 🧠 Inteligencia Lingüística Avanzada
Implementación del motor `_compile_super_regex` para el resaltado automático de actores clave (**Psicólogo/a**, **Víctima**):
* **Insensibilidad Total**: Detecta las palabras ignorando mayúsculas, minúsculas y tildes.
* **Gestión de Género**: Identifica correctamente tanto "Psicólogo" como "Psicóloga" según la configuración del usuario.
* **Precisión de Límites**: Maneja correctamente los signos de puntuación y los espacios especiales de Microsoft Word (`\xa0`), asegurando que solo se resalte al hablante (exigencia de `:` al final).

### 🌍 Sistema de Internacionalización (i18n) Global
Se ha implementado un sistema de **detección automática del idioma** basado en la configuración regional del sistema operativo del usuario.
* **Idiomas Soportados**: 9 idiomas, incluyendo **Español**, **Inglés**, **Alemán**, **Francés**, **Italiano**, **Japonés**, **Portugués**, **Ruso** y **Chino**.
* **Fallback Robusto**: En caso de no encontrar un archivo de traducción específico, el sistema garantiza la estabilidad de la UI volviendo automáticamente al idioma español.

### 📄 Excelencia Documental (Solo DOCX)
Se ha tomado la decisión estratégica de **eliminar la salida en formato .txt**. 
* **Razón**: Centrar todos los recursos del sistema en generar documentos `.docx` de alta calidad institucional, eliminando ruido y simplificando el flujo de trabajo del usuario.

### 🛠️ Mejoras en la Orquestación
* **Mapeo Inteligente**: El sistema ahora detecta archivos ya procesados basándose exclusivamente en la existencia del `.docx` final, evitando duplicidades.
* **Inyección de Género**: Nueva funcionalidad en la interfaz para alternar entre "Psicólogo" y "Psicóloga" antes de iniciar la transcripción.
* **Gestión de Recursos**: Optimización de la limpieza de memoria (GC) y liberación de caché CUDA tras cada archivo procesado.

---

## 🏗️ Arquitectura Técnica Refinada

* **Post-procesamiento Robusto**: Lógica mejorada para la fusión de segmentos y asignación de etiquetas de hablante.
* **Modularización**: Separación clara entre el motor de exportación (`docx_exporter`) y la lógica de negocio (`orchestrator`).
* **Soporte HiDPI**: Mejora en el renderizado de la interfaz para pantallas de alta resolución.

---

## 🔐 Seguridad y Estabilidad

* **Bloqueo Lógico de UI**: Los controles se desactivan inteligentemente durante el proceso para evitar colisiones, manteniendo la estética original.
* **Validación de Entorno**: Control estricto de rutas y archivos críticos para garantizar la portabilidad total del sistema.

---

## 👨‍💻 Créditos

* **Desarrollo:** Pablo Téllez
* **Tecnología:** Whisper + RunMatcher Engine
* **Versión:** 2.0.0 (Marzo 2026)

---

> *Con la Versión 2.0.0, Transcriptor deja de ser una herramienta de conversión para convertirse en un asistente de edición documental quirúrgica, garantizando documentos finales listos para su uso oficial.*
