"""Punto de entrada del sistema Software FJ."""
from logger import configurar_logger
from cliente import Cliente

logger = configurar_logger()


def main():
    logger.info("=== Inicio de la simulación ===")

    Cliente.crear_seguro("Juan Pérez", "1012345678", "juan@correo.com", "3001234567")  # válido
    Cliente.crear_seguro("", "abc", "correo-malo", "123")                               # inválido

    logger.info("=== Fin de la simulación ===")


if __name__ == "__main__":
    main()
