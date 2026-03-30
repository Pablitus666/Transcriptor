_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
	     ____       _     _ _ _                   
	    |  _ \ __ _| |__ | (_) |_ _   _ ___       
	    | |_) / _` | '_ \| | | __| | | / __|      
	    |  __/ (_| | |_) | | | |_| |_| \__ \_ _ _ 
	    |_|   \__,_|_.__/|_|_|\__|\__,_|___(_|_|_)
	_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

================================================================================
|                                                                              |
|   Transcriptor V1.0 - Guía de Inicio Rápido                                  |
|                                                                              |
================================================================================

Esta aplicación automatiza la transcripción de audios a formato Word (.docx),
identificando oradores mediante reglas gramaticales y un sistema de léxico
geográfico y de nombres optimizado para Bolivia.


================================================================================
>> INSTALACIÓN Y ARRANQUE <<
================================================================================

1.  UBICACIÓN DE LA CARPETA
    Copie la carpeta completa "Transcripciones" a su equipo (ej. Escritorio).

2.  INICIO DEL SISTEMA
    Haga doble clic en el archivo:

        --> iniciar.vbs <--

    En la primera ejecución, el sistema:
    *   Configurará los componentes de aceleración por hardware (GPU).
    *   Creará un acceso directo en su Escritorio llamado "Transcriptor".

3.  USO DIARIO
    Utilice el acceso directo del Escritorio para abrir la aplicación.

--------------------------------------------------------------------------------
   IMPORTANTE: NO MOVER LA CARPETA
--------------------------------------------------------------------------------
Una vez ejecutado el sistema por primera vez, no mueva la carpeta original. 
Si necesita cambiarla de ubicación, vuelva a realizar el paso 1 y 2 desde 
la copia de respaldo.
--------------------------------------------------------------------------------


================================================================================
>> INSTRUCCIONES DE USO <<
================================================================================

*   SELECCIÓN DE AUDIOS (Drag & Drop)
    Puede arrastrar una carpeta con audios o un archivo individual directamente
    hacia la aplicación para cargar la ruta de forma instantánea.

*   PLANTILLA DOCX (Opcional)
    Si posee una plantilla institucional, selecciónela en el segundo campo.
    El sistema recordará su elección para futuros usos.

*   MODELO Y GÉNERO
    - Modelo: Se recomienda "large-v3" para precisión técnica.
    - Profesional: Seleccione "Psicólogo" o "Psicóloga" según corresponda 
      para la etiqueta del entrevistador en el documento final.

*   PROCESAMIENTO
    Haga clic en "Transcribir". El sistema utilizará la tarjeta de video 
    (NVIDIA CUDA) para procesar los audios en segundo plano.


================================================================================
>> REQUISITOS TÉCNICOS <<
================================================================================

1.  CONEXIÓN A INTERNET: Requerida ÚNICAMENTE la primera vez que transcriba
    para descargar los modelos de IA. Luego el sistema es 100% OFFLINE.

2.  HARDWARE: Optimizado para tarjetas de video NVIDIA.


================================================================================
>> RESULTADOS <<
================================================================================

Los documentos finales se guardarán automáticamente en la MISMA CARPETA donde
se encuentran sus audios originales, con el prefijo:

    --> ENTREVISTA INFORMATIVA_ <--

Formato: Arial 11, interlineado sencillo y oradores resaltados en negrita.

================================================================================

Desarrollado por: Pablo Téllez A.
Versión: 1.0.0 (Marzo 2026)
