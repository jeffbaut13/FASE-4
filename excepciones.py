######funcion de este archivo: concentrar todos los errores personalizados del sistema en un solo lugar.
"""Excepciones personalizadas del sistema Software FJ."""

class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Datos inválidos o faltantes de un cliente."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros inválidos al crear o configurar un servicio."""
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
