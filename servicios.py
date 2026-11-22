"""Define la clase base de los servicios y sus tipos especializados."""
import logging
import math
from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


# El mismo registrador permite consultar los eventos de todos los servicios.
logger = logging.getLogger("SoftwareFJ")


def _es_numero_finito(valor):
    """Comprueba números aceptados sin dejar escapar errores de conversión."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return False
    try:
        return math.isfinite(valor)
    except OverflowError:
        return False


class Servicio(Entidad):
    """Clase base con los datos y operaciones comunes de cada servicio.

    Las clases hijas deben definir su propia forma de describirse.
    """

    # Lleva la cuenta de los servicios para asignar identificadores consecutivos.
    _contador_id = 0

    def __init__(self, nombre, tarifa_hora, disponible=True):
        """Valida los datos básicos y prepara un nuevo servicio.

        ``nombre`` identifica el servicio, ``tarifa_hora`` es su precio por hora
        y ``disponible`` indica si se puede reservar en este momento.
        """

        # El nombre debe tener texto y se guarda sin espacios en los extremos.
        if not isinstance(nombre, str) or not nombre.strip():
            logger.error("Fallo al crear servicio: nombre invalido.")
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacio.")

        if (
            not _es_numero_finito(tarifa_hora)
            or tarifa_hora <= 0
        ):
            logger.error(f"Fallo al crear '{nombre}': Tarifa invalida ({tarifa_hora})")
            raise ServicioInvalidoError("La tarifa debe ser mayor a cero")

        if not isinstance(disponible, bool):
            logger.error("Fallo al crear '%s': disponibilidad invalida (%s)", nombre, disponible)
            raise ServicioInvalidoError("La disponibilidad debe ser verdadera o falsa")

        Servicio._contador_id += 1
        super().__init__(Servicio._contador_id)

        # Los atributos privados guardan los valores ya validados y normalizados.
        self.__nombre = nombre.strip()
        self.__tarifa_hora = tarifa_hora
        self.__disponible = disponible
        logger.info(f"Servicio base inicializado: ID {self.id} - {self.__nombre}")

    @property
    def nombre(self):
        """Devuelve el nombre del servicio; solo se puede consultar."""
        return self.__nombre

    @property
    def tarifa_hora(self):
        """Devuelve la tarifa por una hora de servicio."""
        return self.__tarifa_hora

    @property
    def disponible(self):
        """Indica si el servicio puede reservarse."""
        return self.__disponible
    
    @disponible.setter
    def disponible(self, valor):
        """Actualiza la disponibilidad y exige un valor verdadero o falso."""
        if not isinstance(valor, bool):
            logger.error("No se pudo actualizar la disponibilidad del servicio: %s", valor)
            raise ServicioInvalidoError("La disponibilidad debe ser verdadera o falsa")
        self.__disponible = valor
        
    def calcular_costo(self, horas=None, impuesto=0.19, descuento=0.0):
        """Calcula el costo final usando horas, impuesto y descuento.

        ``impuesto`` y ``descuento`` se expresan como proporciones: por ejemplo,
        ``0.19`` representa el 19 %. Los argumentos opcionales permiten llamar
        este método con distintas combinaciones de horas, impuesto y descuento.
        El resultado se redondea a un decimal.
        """
        if (
            not _es_numero_finito(horas)
            or horas <= 0
        ):
            logger.error(f"Horas invalidas ({horas}) calculo del costo")
            raise CalculoInconsistenteError("La hora debe ser mayor a cero")

        # Cada porcentaje debe ser un número finito y no negativo.
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if (
                not _es_numero_finito(valor)
                or valor < 0
            ):
                logger.error("%s invalido (%s) en calculo del costo", nombre, valor)
                raise CalculoInconsistenteError(
                    f"El {nombre} debe ser un número no negativo"
                )

        if descuento > 1:
            logger.error("Descuento invalido (%s) en calculo del costo", descuento)
            raise CalculoInconsistenteError("El descuento no puede ser mayor al 100 %")

        # Primero se calcula el precio por horas y luego se aplica el descuento.
        try:
            subtotal = self.__tarifa_hora * horas
            valor_descuento = subtotal * descuento
            base_gravable = subtotal - valor_descuento
            # El impuesto se suma después del descuento y antes del redondeo final.
            total = base_gravable * (1 + impuesto)
        except OverflowError as error:
            logger.exception("El calculo del costo excedio el rango permitido")
            raise CalculoInconsistenteError(
                "El costo supera el rango numérico permitido"
            ) from error

        if not math.isfinite(total):
            logger.error("El calculo produjo un costo no finito (%s)", total)
            raise CalculoInconsistenteError("El costo calculado no es finito")
        return round(total, 1)

    @abstractmethod
    def describir(self):
        """Obliga a cada servicio especializado a construir su descripción."""
        pass


class AlquilerEquipo(Servicio):
    """Servicio que permite alquilar un equipo identificado por su tipo."""

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo=None, disponible=True):
        """Crea un alquiler de equipo y valida la descripción del equipo."""
        # El tipo indica qué clase de equipo se está ofreciendo en alquiler.
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            logger.error(f"Tipo de equipo invalido ({tipo_equipo}) al crear servicio")
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacio.")
        super().__init__(nombre, tarifa_hora, disponible)
        self.__tipo_equipo = tipo_equipo.strip()
        logger.info(f"AlquilerEquipo creado: {self.nombre} (Equipo: {self.__tipo_equipo})")

    @property
    def tipo_equipo(self):
        """Devuelve el tipo de equipo que se ofrece en alquiler."""
        return self.__tipo_equipo

    def calcular_costo(self, horas=None, impuesto=0.19, descuento=0.0):
        """Calcula el alquiler con la tarifa común y opciones de impuesto."""
        return super().calcular_costo(horas, impuesto, descuento)

    def describir(self):
        """Devuelve el equipo, su tarifa y su estado de disponibilidad."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Equipo]: {self.nombre} | "
            f"Tipo: {self.__tipo_equipo} | Tarifa: ${self.tarifa_hora:.1f}/h |  {estado}"
        )
class ReservaSala(Servicio):
    """Servicio que permite reservar una sala con capacidad definida."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None, disponible=True):
        """Crea una sala y exige que su capacidad sea un entero positivo."""
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            logger.error(f"Capacidad invalidad ({capacidad}) al crear la sala.")
            raise ServicioInvalidoError("La capacidad deber ser un numero entero mayor a cero.")
        super().__init__(nombre, tarifa_hora, disponible)
        # Se conserva la cantidad máxima de personas que pueden usar la sala.
        self.__capacidad = capacidad
        logger.info(f"ReservaSala creada: {self.nombre} (Capacidad: {self.__capacidad} personas)")

    @property
    def capacidad(self):
        """Devuelve el máximo de personas admitidas en la sala."""
        return self.__capacidad

    def calcular_costo(self, horas=None, impuesto=0.19, descuento=0.0):
        """Calcula la sala con la tarifa común y opciones de impuesto."""
        return super().calcular_costo(horas, impuesto, descuento)

    def describir(self):
        """Devuelve la capacidad, la tarifa y el estado actual de la sala."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Sala]: {self.nombre}  |  "
            f"Capacidad: {self.__capacidad} Pers.  |  Tarifa: ${self.tarifa_hora:.1f}/h | {estado}"
        )

class Asesoria(Servicio):
    """Servicio especializado en asesorias."""

    def __init__(self, nombre=None, tarifa_hora=None, especialidad=None, disponible=True):
        """Crea una asesoría y valida que tenga una especialidad indicada."""
        if not isinstance(especialidad, str) or not especialidad.strip():
            logger.error(f"Especialidad invalida ({especialidad} al crear la asesoria.)")
            raise ServicioInvalidoError("La especialidad no puede estar vacia.")
        super().__init__(nombre, tarifa_hora, disponible)
        self.__especialidad = especialidad.strip()
        logger.info(f"Asesoria creada: {self.nombre} (Area: {self.__especialidad})")

    @property
    def especialidad(self):
        """Devuelve el área de conocimiento de la asesoría."""
        return self.__especialidad

    def calcular_costo(self, horas=None, impuesto=0.19, descuento=0.0):
        """Calcula la asesoría con la tarifa común y opciones de descuento."""
        return super().calcular_costo(horas, impuesto, descuento)

    def describir(self):
        """Devuelve el área, la tarifa y la disponibilidad de la asesoría."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Asesoria]: {self.nombre}  |  Area: {self.__especialidad}  |  Tarifa: ${self.tarifa_hora:.1f}/h  |  {estado}"
        )


if __name__ == "__main__":
    # Estos objetos de ejemplo muestran cómo se crean los servicios disponibles.
    sala = ReservaSala("Sala Juntas A", 5000, 10)
    equipo = AlquilerEquipo("Portatil Dell", 20000, "Laptop")
    asesoria = Asesoria("Consultoria Cloud", 80000, "AWS")

    # Se imprimen las descripciones y se calculan costos de ejemplo.
    print (sala.describir())
    print ("Costo sala (2h con IVA):", sala.calcular_costo(2))
    print(equipo.describir())
    print("Costo equipo (3h con 10% desc):", equipo.calcular_costo(3, descuento=0.10))
    print(asesoria.describir())

    # Se comprueba que una tarifa inválida se reporte como excepción propia.
    try:
        ServicioInvalido = Asesoria("Mala", -5000, "Redes")
    except ServicioInvalidoError as e: 
        print ("Alarma funciono:", e)   























