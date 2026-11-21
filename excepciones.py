"""Reúne las excepciones propias para informar errores del sistema."""

class SoftwareFJError(Exception):
    """Error general del que heredan las excepciones de Software FJ."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Indica que falta un dato del cliente o que no cumple su formato."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Indica que un servicio recibió datos de creación no válidos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Intento de reserva incorrecto o con datos inconsistentes."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación no permitida en el estado actual (ej. cancelar una reserva ya cancelada)."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Error en cálculos de costos, impuestos o descuentos."""
    pass
