"""Modela una reserva y sus cambios de estado dentro del sistema."""
import logging
import math
from enum import Enum

from entidad import Entidad
from excepciones import (
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from cliente import Cliente
from servicios import Servicio


logger = logging.getLogger("SoftwareFJ")


def _es_numero_finito(valor):
    """Comprueba que la duración sea un número finito sin conversión insegura."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return False
    try:
        return math.isfinite(valor)
    except OverflowError:
        return False


class EstadoReserva(Enum):
    """Estados posibles durante la vida de una reserva."""

    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Reserva(Entidad):
    """Relaciona un cliente con un servicio y controla su proceso de reserva."""

    _contador_id = 0

    def __init__(self, cliente=None, servicio=None, horas=None):
        """Crea una reserva pendiente y la asocia a la lista del cliente.

        ``cliente`` y ``servicio`` deben ser objetos del sistema, y ``horas``
        debe ser un número positivo y finito.
        """
        if not isinstance(cliente, Cliente):
            logger.error("No se pudo crear la reserva: cliente invalido (%s)", cliente)
            raise ReservaInvalidaError("La reserva requiere un cliente válido")

        if not isinstance(servicio, Servicio):
            logger.error("No se pudo crear la reserva: servicio invalido (%s)", servicio)
            raise ReservaInvalidaError("La reserva requiere un servicio válido")

        if (
            not _es_numero_finito(horas)
            or horas <= 0
        ):
            logger.error("No se pudo crear la reserva: duracion invalida (%s)", horas)
            raise ReservaInvalidaError("La duración debe ser un número mayor a cero")

        if not servicio.disponible:
            logger.error("No se pudo reservar el servicio %s porque no esta disponible", servicio.id)
            raise ServicioNoDisponibleError("El servicio solicitado no está disponible")

        Reserva._contador_id += 1
        super().__init__(Reserva._contador_id)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = EstadoReserva.PENDIENTE
        self.__costo_total = None
        cliente.agregar_reserva(self)
        logger.info(
            "Reserva %s creada para cliente %s y servicio %s",
            self.id,
            cliente.id_cliente,
            servicio.id,
        )

    @property
    def cliente(self):
        """Devuelve el cliente relacionado con la reserva."""
        return self.__cliente

    @property
    def servicio(self):
        """Devuelve el servicio relacionado con la reserva."""
        return self.__servicio

    @property
    def horas(self):
        """Devuelve la duración reservada."""
        return self.__horas

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self.__estado

    @property
    def costo_total(self):
        """Devuelve el costo calculado al procesar la reserva, si existe."""
        return self.__costo_total

    def confirmar(self):
        """Confirma una reserva pendiente si el servicio sigue disponible."""
        if self.__estado is not EstadoReserva.PENDIENTE:
            logger.error(
                "No se pudo confirmar la reserva %s desde el estado %s",
                self.id,
                self.__estado.value,
            )
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes"
            )

        if not self.__servicio.disponible:
            logger.error(
                "No se pudo confirmar la reserva %s: servicio no disponible",
                self.id,
            )
            raise ServicioNoDisponibleError("El servicio solicitado no está disponible")

        self.__estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva %s confirmada", self.id)
        return self

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self.__estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            logger.error(
                "No se pudo cancelar la reserva %s desde el estado %s",
                self.id,
                self.__estado.value,
            )
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas pendientes o confirmadas"
            )

        self.__estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada", self.id)
        return self

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Calcula el costo y completa una reserva previamente confirmada.

        Los argumentos opcionales se envían al cálculo del servicio. Si el
        cálculo falla, la reserva conserva su estado confirmado para permitir
        corregir los valores y volver a procesarla.
        """
        if self.__estado is not EstadoReserva.CONFIRMADA:
            logger.error(
                "No se pudo procesar la reserva %s desde el estado %s",
                self.id,
                self.__estado.value,
            )
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas confirmadas"
            )

        costo = self.__servicio.calcular_costo(self.__horas, impuesto, descuento)
        self.__costo_total = costo
        self.__estado = EstadoReserva.COMPLETADA
        logger.info("Reserva %s procesada. Costo total: %s", self.id, costo)
        return costo

    def describir(self):
        """Devuelve un resumen de la reserva, sus participantes y su estado."""
        costo = (
            f"${self.__costo_total:.1f}"
            if self.__costo_total is not None
            else "Pendiente de cálculo"
        )
        return (
            f"Reserva #{self.id} | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Horas: {self.__horas} | "
            f"Estado: {self.__estado.value} | Costo: {costo}"
        )
