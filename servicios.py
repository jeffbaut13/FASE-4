"""Define la clase base de los servicios y sus tipos especializados."""
import logging
from abc import abstractmethod
from entidad import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


# El mismo registrador permite consultar los eventos de todos los servicios.
logger = logging.getLogger("SoftwareFJ")


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

        Servicio._contador_id += 1
        super().__init__(Servicio._contador_id)

        # El nombre debe tener texto y se guarda sin espacios en los extremos.
        if not isinstance(nombre, str) or not nombre.strip():
            logger.error("Fallo al crear servicio: nombre invalido.")
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacio.")
        
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <=0:
            logger.error(f"Fallo al crear '{nombre}': Tarifa invalida ({tarifa_hora})")
            raise ServicioInvalidoError("La tarifa debe ser mayor a cero")

        # Los atributos privados guardan los valores ya validados y normalizados.
        self.__nombre = nombre.strip()
        self.__tarifa_hora = float(tarifa_hora)
        self.__disponible = bool(disponible)
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
        """Actualiza el estado de disponibilidad y lo convierte a booleano."""
        self.__disponible = bool(valor)
        
    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0):
        """Calcula el costo final usando horas, impuesto y descuento.

        ``impuesto`` y ``descuento`` se expresan como proporciones: por ejemplo,
        ``0.19`` representa el 19 %. El resultado se redondea a un decimal.
        """
        if not isinstance(horas, (int, float)) or horas <= 0:
            logger.error(f"Horas invalidas ({horas}) calculo del costo")
            raise CalculoInconsistenteError("La hora debe ser mayor a cero")

        # Se evita aplicar un impuesto negativo o un descuento fuera del rango 0-1.
        if impuesto < 0 or descuento < 0 or descuento > 1:
            logger.error(f"Impuesto ({impuesto}) o descuento ({descuento}) invalido en calculo del costo")
            raise CalculoInconsistenteError("Impuesto o descuento invalido")

        # Primero se calcula el precio por horas y luego se aplica el descuento.
        subtotal = self.__tarifa_hora * horas
        valor_descuento = subtotal * descuento
        base_gravable = subtotal - valor_descuento
        # El impuesto se suma después del descuento y antes del redondeo final.
        total = base_gravable * (1 + impuesto)
        return round(total, 1)

    @abstractmethod
    def describir(self):
        """Obliga a cada servicio especializado a construir su descripción."""
        pass 
class AlquilerEquipo(Servicio):
    """Servicio que permite alquilar un equipo identificado por su tipo."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, disponible=True):
        """Crea un alquiler de equipo y valida la descripción del equipo."""
        super().__init__(nombre, tarifa_hora, disponible)
        # El tipo indica qué clase de equipo se está ofreciendo en alquiler.
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            logger.error(f"Tipo de equipo invalido ({tipo_equipo}) al crear servicio")
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacio.")
        self.__tipo_equipo = tipo_equipo.strip()
        logger.info(f"AlquilerEquipo creado: {self.nombre} (Equipo: {self.__tipo_equipo})")

    @property
    def tipo_equipo(self):
        """Devuelve el tipo de equipo que se ofrece en alquiler."""
        return self.__tipo_equipo

    def describir(self):
        """Devuelve el equipo, su tarifa y su estado de disponibilidad."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Equipo]: {self.nombre} | "
            f"Tipo: {self.__tipo_equipo} | Tarifa: ${self.tarifa_hora:.1f}/h |  {estado}"
        )
class ReservaSala(Servicio):
    """Servicio que permite reservar una sala con capacidad definida."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        """Crea una sala y exige que su capacidad sea un entero positivo."""
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            logger.error(f"Capacidad invalidad ({capacidad}) al crear la sala.")
            raise ServicioInvalidoError("La capacidad deber ser un numero entero mayor a cero.")
        # Se conserva la cantidad máxima de personas que pueden usar la sala.
        self.__capacidad = capacidad
        logger.info(f"ReservaSala creada: {self.nombre} (Capacidad: {self.__capacidad} personas)")

    @property
    def capacidad(self):
        """Devuelve el máximo de personas admitidas en la sala."""
        return self.__capacidad

    def describir(self):
        """Devuelve la capacidad, la tarifa y el estado actual de la sala."""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Sala]: {self.nombre}  |  "
            f"Capacidad: {self.__capacidad} Pers.  |  Tarifa: ${self.tarifa_hora:.1f}/h | {estado}"
        )

class Asesoria(Servicio):
    """Servicio especializado en asesorias."""

    def __init__(self, nombre, tarifa_hora, especialidad, disponible=True):
        """Crea una asesoría y valida que tenga una especialidad indicada."""
        super().__init__(nombre, tarifa_hora, disponible)

        if not isinstance(especialidad, str) or not especialidad.strip():
            logger.error(f"Especialidad invalida ({especialidad} al crear la asesoria.)")
            raise ServicioInvalidoError("La especialidad no puede estar vacia.")
        self.__especialidad = especialidad.strip()
        logger.info(f"Asesoria creada: {self.nombre} (Area: {self.__especialidad})")

    @property
    def especialidad(self):
        """Devuelve el área de conocimiento de la asesoría."""
        return self.__especialidad

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


























