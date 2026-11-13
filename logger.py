"""Configuración central del archivo de logs de Software FJ."""
import logging

def configurar_logger(nombre_archivo="logs.txt"):
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    ##### Evita duplicar si se llama más de una vez#####
    if not logger.handlers:
        manejador = logging.FileHandler(nombre_archivo, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)

    return logger
