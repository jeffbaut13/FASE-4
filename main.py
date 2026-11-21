"""Inicia una demostración del registro de clientes de Software FJ.

La configuración del registrador se prepara al cargar este módulo para que
los mensajes de la simulación queden guardados en el archivo de logs.
"""
from logger import configurar_logger
from cliente import Cliente

logger = configurar_logger()


def main():
    """Ejecuta ejemplos de registro correcto e incorrecto de clientes."""
    logger.info("=== Inicio de la simulación ===")

    # El primer ejemplo usa datos válidos y el segundo activa las validaciones.
    Cliente.crear_seguro("Juan Pérez", "1012345678", "juan@correo.com", "3001234567")  # válido
    Cliente.crear_seguro("", "abc", "correo-malo", "123")                               # inválido

    logger.info("=== Fin de la simulación ===")


if __name__ == "__main__":
    # Ejecuta la simulación solo cuando este archivo se inicia directamente.
    main()
