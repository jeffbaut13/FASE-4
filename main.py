"""Ejecuta ejemplos de clientes, servicios y reservas de Software FJ."""
from logger import configurar_logger
from cliente import Cliente
from excepciones import SoftwareFJError
from reserva import Reserva
from servicios import AlquilerEquipo, Asesoria, ReservaSala


logger = configurar_logger()


def _ejecutar_operacion(nombre, accion):
    """Ejecuta una operación del ejemplo y registra errores del sistema.

    Los errores esperados se informan y no detienen las siguientes
    operaciones. Los errores inesperados se dejan visibles para corregirlos.
    """
    print(f"\n{nombre}:")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        logger.exception("La operacion '%s' no se pudo completar", nombre)
        print(f"[ERROR] {error}")
        resultado = None
    else:
        logger.info("La operacion '%s' se completo", nombre)
        if resultado is not None:
            print(f"[OK] {resultado}")
    finally:
        logger.info("Intento de operacion finalizado: %s", nombre)
    return resultado


def main():
    """Simula más de diez operaciones válidas e inválidas sin detenerse."""
    logger.info("=== Inicio de la simulación integral ===")
    operaciones = []

    def ejecutar(nombre, accion):
        resultado = _ejecutar_operacion(nombre, accion)
        operaciones.append((nombre, resultado))
        return resultado

    cliente = ejecutar(
        "1. Registrar cliente válido",
        lambda: Cliente("Juan Pérez", "1012345678", "juan@correo.com", "3001234567"),
    )
    ejecutar(
        "2. Intentar registrar cliente inválido",
        lambda: Cliente.crear_seguro("", "abc", "correo-malo", "123"),
    )

    sala = ejecutar(
        "3. Crear sala disponible",
        lambda: ReservaSala("Sala Juntas A", 5000, 10),
    )
    equipo = ejecutar(
        "4. Crear alquiler de equipo",
        lambda: AlquilerEquipo("Portátil Dell", 20000, "Laptop"),
    )
    ejecutar(
        "5. Crear asesoría especializada",
        lambda: Asesoria("Consultoría Cloud", 80000, "AWS"),
    )
    ejecutar(
        "6. Intentar crear servicio inválido",
        lambda: AlquilerEquipo("Equipo sin tipo", 20000, ""),
    )

    reserva_sala = ejecutar(
        "7. Crear reserva de sala",
        lambda: Reserva(cliente, sala, 2),
    )
    ejecutar("8. Confirmar reserva de sala", reserva_sala.confirmar)
    ejecutar("9. Procesar reserva con impuesto", reserva_sala.procesar)

    reserva_equipo = ejecutar(
        "10. Crear reserva de equipo",
        lambda: Reserva(cliente, equipo, 3),
    )
    ejecutar("11. Cancelar reserva de equipo", reserva_equipo.cancelar)
    ejecutar(
        "12. Intentar cancelar reserva completada",
        reserva_sala.cancelar,
    )

    servicio_no_disponible = ejecutar(
        "13. Crear asesoría no disponible",
        lambda: Asesoria("Asesoría de redes", 60000, "Redes", disponible=False),
    )
    ejecutar(
        "14. Intentar reservar servicio no disponible",
        lambda: Reserva(cliente, servicio_no_disponible, 1),
    )
    ejecutar(
        "15. Intentar reservar duración inválida",
        lambda: Reserva(cliente, sala, 0),
    )

    logger.info(
        "=== Fin de la simulación: %s operaciones ejecutadas ===",
        len(operaciones),
    )
    print(f"\nSimulación finalizada: {len(operaciones)} operaciones.")
    return operaciones


if __name__ == "__main__":
    main()
