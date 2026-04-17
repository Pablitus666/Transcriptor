# 🚀 Transcriptor — Notas de Versión

---

## 💎 Versión 1.1.0 — Edición Élite (Abril 2026)
Esta actualización consolida el sistema para despliegue institucional:
- **Instalador Unificado:** El archivo `Transcriptor_Setup.exe` ahora integra el entorno `whisper_env` completo para evitar corrupciones.
- **Firma Digital SHA256:** El instalador cuenta con la firma digital verificada.
- **Portabilidad Certificada:** Validado para funcionar desde unidades externas e internas (C:, I:, etc.) sin pérdida de configuración.
- **Instalación Raíz:** El programa se instala en `C:\Transcriptor` para garantizar permisos totales de escritura.

---

## 💎 Versión 1.0.1 — Edición Élite (Abril 2026)
Esta actualización se centra en la identidad visual y la portabilidad del sistema:
- **Icono Multi-capa de Alta Resolución:** Se ha corregido el pixelado en Windows mediante un icono de 7 capas (16px a 256px) para una nitidez absoluta en HiDPI.
- **Portabilidad Dinámica Mejorada:** El sistema detecta su ubicación de forma inteligente, permitiendo renombrar o mover la carpeta contenedora sin romper los enlaces internos.
- **Firma Digital SHA256:** El ejecutable oficial `Transcriptor.exe` está firmado y sellado digitalmente.

---

## 💎 Versión 1.0.0 — Edición Élite (Lanzamiento Profesional - Marzo 2026)

Esta versión marca la transición definitiva de un script de automatización a un software de **Grado Institucional Blindado**. Se han implementado capas de seguridad y profesionalismo para garantizar la integridad de la propiedad intelectual y una experiencia de usuario premium.

### 🛡️ Blindaje y Protección de Código
- **Compilación .pyd:** Todos los módulos de la aplicación (`core`, `utils`, `exporters`, `gui`) han sido convertidos a binarios protegidos.
- **worker.pyd:** El núcleo del procesamiento asíncrono ahora es un binario blindado, ocultando la "receta" interna del motor de IA.

### 🖋️ Firma Digital y Seguridad
- **SHA256 Code Signing:** Implementación de firma digital con sello de tiempo en el instalador y el ejecutable principal.
- **Identidad Verificada:** El software es reconocido por Windows porque esta firmado digitalmeente, eliminando alertas de seguridad sospechosas.

### 🔇 Silencio Operativo (Parche Élite)
- **Clase SilentPopen:** Inyección de un parche a nivel de sistema que silencia globalmente las ventanas de consola de FFmpeg y librerías de IA, eliminando parpadeos molestos durante el uso.

## 📦 Distribución Modular y Portátil
Esta versión utiliza una arquitectura de **Distribución Modular** para facilitar el manejo de archivos pesados de IA:

1.  **Instalador Ligero**: El archivo `Transcriptor_Setup.exe` instala solo el núcleo del programa.
2.  **Motor Externo**: Las carpetas `whisper_env` y `models_cache` se distribuyen por separado. 
3.  **Configuración Final**: Para que el programa funcione, el usuario debe copiar estas dos carpetas dentro del directorio de instalación (`C:\Transcriptor`).

---

## 🛡️ Blindaje y Protección de Código


Esta versión inicial establece la arquitectura base del sistema, centrada en la integración de motores de reconocimiento de voz de alta precisión y lógica aplicada al diálogo judicial.

---

## 🎯 Mejoras Técnicas Implementadas (Versión Base)

### 🧠 Motor de Lógica Gramatical
Se ha desarrollado un sistema de control de turnos que analiza la estructura gramatical de la conversación.
* **Funcionamiento**: Detecta signos de interrogación para anticipar cambios de orador.

### ⚛️ Fusión Atómica de Segmentos
Implementación de un algoritmo de consolidación que unifica textos del mismo hablante.

### 🏎️ Integración de WhisperX y CUDA
Optimización para NVIDIA CUDA 12.1, permitiendo el procesamiento acelerado por GPU.

### 📍 Diccionario Nacional de Bolivia
Integración de 934 nombres/apellidos comunes en Bolivia y 1,120 calles de Tarija.

---

## 👨‍💻 Créditos

* **Desarrollo:** Walter Pablo Téllez Ayala
* **Tecnología:** AI Blindada + WhisperX
* **Versión:** 1.0.1 Edición Élite (Marzo 2026)

---

> *Transcriptor Edición Élite combina seguridad binaria con inteligencia artificial de vanguardia para entornos judiciales de alta exigencia.*
