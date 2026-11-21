"""Configuración central del archivo de logs de Software FJ."""
import logging

def configurar_logger(nombre_archivo="logs.txt"):
    """Prepara el registrador del sistema y lo devuelve.

    ``nombre_archivo`` indica dónde guardar los mensajes. El nivel INFO permite
    registrar información general, advertencias y errores.
    """
    # Se reutiliza un único registrador para los módulos de Software FJ.
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    # Se crea un manejador solo una vez para no repetir mensajes en el archivo.
    if not logger.handlers:
        # El archivo se abre con UTF-8 para conservar correctamente los acentos.
        manejador = logging.FileHandler(nombre_archivo, encoding="utf-8")
        # Cada línea incluye fecha, nivel, nombre del registrador y mensaje.
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger
