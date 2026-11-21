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
    """Indica que se intentó usar un servicio marcado como no disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Indica que una reserva tiene datos incompletos o incompatibles."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Indica que una acción no corresponde al estado actual del objeto."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Indica que no se puede realizar un cálculo con los valores recibidos."""
    pass
