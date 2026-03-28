# 🚀 Transcriptor — Release Notes (V1.0)

---

## ✨ Versión 1.0.0

Esta versión marca el inicio oficial de **Transcriptor**, integrando **WhisperX**, aceleración por GPU y un sistema de lógica gramatical para la identificación de oradores.

---

## 🎯 Novedades V1.0.0

### 🧠 Cerebro Gramatical de Turnos
El sistema entiende la estructura del diálogo. Si el Profesional pregunta, el script intenta corregir automáticamente a la IA y asignar la respuesta a la Víctima.

### ⚛️ Fusión Atómica de Oradores
Se ha implementado un nuevo motor de consolidación de texto que erradica la redundancia.
* **Resultado**: Eliminación total de etiquetas duplicadas (Psicóloga: ... Psicóloga: ...). El documento final fluye como una entrevista real, limpia y sin interrupciones visuales.

### 🏎️ Aceleración por GPU (NVIDIA CUDA 12.1)
Migración completa al entorno `whisper_env` optimizado para tarjetas de video.
* **Rendimiento**: Procesamiento hasta 10 veces más rápido que las versiones anteriores. Audios de 30 minutos se transcriben ahora en menos de 3 minutos con el modelo `large-v3`.

### 📍 Diccionario Geográfico de Tarija (OSM)
Integración de un léxico local de alta precisión.
* **Base de datos**: Más de **1,100 nombres de calles y avenidas** extraídos de OpenStreetMap.
* **Efecto**: Capitalización y ortografía automática perfecta para direcciones locales de Tarija, Bolivia (FELCV, SLIM, barrios periféricos).

### 🖋️ Motor WhisperX V30 (Alineación Fonética)
Sustitución del motor base por **WhisperX**.
* **Precisión**: Alineación a nivel de palabra con una sincronía de ±30ms, permitiendo que las negritas y el resaltado sean quirúrgicos.

---

## 🏗️ Mejoras en la Robustez

* **Blindaje de Tablas**: El exportador ahora ignora quirúrgicamente las tablas de cabecera para proteger los datos institucionales sensibles.
* **Suavizado Anti-Flicker**: Eliminación de cambios erróneos de orador que duran menos de 0.5 segundos.
* **Soporte Arial 11 Institucional**: Forzado de fuente y tamaño en todos los párrafos generados para cumplimiento normativo inmediato.

---

## 👨‍💻 Créditos

* **Desarrollo:** Walter Pablo Téllez Ayala
* **Tecnología:** WhisperX + Grammatical Turn Engine V40
* **Versión:** 4.0.0 (Edición Forense - Marzo 2026)

---

> *Con la Versión 4.0.0, Transcriptor alcanza el estándar de oro en transcripción forense judicial para Bolivia, combinando potencia de GPU con inteligencia lingüística aplicada.*
