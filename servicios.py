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

    @property #antes de ejecutar el codigo este hace una validacion de que es correcto
    def nombre(self):
        """Devolver nombre de servicio"""
        return self.__nombre #retorna el nombre
    @property
    def tarifa_hora(self):
        """Devolver tarifa por hora"""
        return self.__tarifa_hora #retorna la tarifa
    @property
    def disponible(self):
        """Indica si esta disponible el servicio"""
        return self.__disponible #de numero a disponible
    
    @disponible.setter
    def disponible(self, valor):
        """Disponibilidad Actual del servicio"""
        self.__disponible = bool(valor) #actualiza la disponibilidad del servicio
        
    def calcular_costo(self,horas, impuesto=0.19, descuento=0.0):
        """Calcular el costo total con los parametros opcionales, como el iva"""
        #hora positiva
        if not isinstance(horas, (int, float)) or horas <= 0:
            logger.error(f"Horas invalidas ({horas}) calculo del costo")
            raise CalculoInconsistenteError("La hora debe ser mayor a cero")

        if impuesto < 0 or descuento < 0 or descuento > 1:
            logger.error(f"Impuesto ({impuesto}) o descuento ({descuento}) invalido en calculo del costo")
            raise CalculoInconsistenteError("Impuesto o descuento invalido")

        # lo mas sencillo, los totales
        subtotal = self.__tarifa_hora * horas
        valor_descuento = subtotal * descuento
        base_gravable = subtotal - valor_descuento
        total = base_gravable * (1 + impuesto)
        return round(total, 1)

    @abstractmethod
    def describir(self):
        """Metodo obligatorio"""
        pass 
class AlquilerEquipo(Servicio):
    """Servicio especializado"""
    def __init__(self, nombre, tarifa_hora, tipo_equipo, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
    #tipo de equipo el texto no debe de estar vacio
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            logger.error(f"Tipo de equipo invalido ({tipo_equipo}) al crear servicio")
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacio.")        
        self.__tipo_equipo = tipo_equipo.strip() #guarda el ripo de equipo
        logger.info(f"AlquilerEquipo creado: {self.nombre} (Equipo: {self.__tipo_equipo})")
    @property 
    def tipo_equipo(self):
        """Devolver el tipo de equipo alquilado (lectura)"""
        return self.__tipo_equipo #devuelve el equipo alquilado
    def describir(self):
        """Descripcion del equipo alquilado"""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Equipo]: {self.nombre} | "
            f"Tipo: {self.__tipo_equipo} | Tarifa: ${self.tarifa_hora:.1f}/h |  {estado}"
        ) #retorna la descripcion del equipo alquilado
class ReservaSala(Servicio):
    """Servicio especializado"""
    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        """Iniciación de sala (según capacidad)"""
        super().__init__(nombre, tarifa_hora, disponible)
        #llamamos a la clase padre

        #validamos que la capacidad sea un numero entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            logger.error(f"Capacidad invalidad ({capacidad}) al crear la sala.") 
            raise ServicioInvalidoError("La capacidad deber ser un numero entero mayor a cero.")
        self.__capacidad = capacidad #la guarda
        logger.info(f"ReservaSala creada: {self.nombre} (Capacidad: {self.__capacidad} personas)")


    #exactamente igual que la otra clase
    @property
    def capacidad(self):
        """Devuelve la capacidad maxima de la sala (Lectura)"""
        return self.__capacidad

    def describir(self):
        """Descripcion de sala reservada"""
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Sala]: {self.nombre}  |  "
            f"Capacidad: {self.__capacidad} Pers.  |  Tarifa: ${self.tarifa_hora:.1f}/h | {estado}"
        ) #nuevamente esto retorna la descripcion de la sala 

class Asesoria(Servicio):
    """Servicio especializado en asesorias."""
    def __init__(self, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)

        if not isinstance(especialidad, str) or not especialidad.strip():
            logger.error(f"Especialidad invalida ({especialidad} al crear la asesoria.)")
            raise ServicioInvalidoError("La especialidad no puede estar vacia.")
        self.__especialidad = especialidad.strip() 
        logger.info(f"Asesoria creada: {self.nombre} (Area: {self.__especialidad})")

    @property
    def especialidad(self):
        """Devuelve la especialidad 
        (lectura)"""
        return self.__especialidad

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio #{self.id} [Asesoria]: {self.nombre}  |  Area: {self.__especialidad}  |  Tarifa: ${self.tarifa_hora:.1f}/h  |  {estado}"
        )

if __name__ == "__main__":
    sala = ReservaSala("Sala Juntas A", 5000, 10)
    equipo = AlquilerEquipo("Portatil Dell", 20000, "Laptop")
    asesoria = Asesoria("Consultoria Cloud", 80000, "AWS")

    print (sala.describir())
    print ("Costo sala (2h con IVA):", sala.calcular_costo(2))
    print(equipo.describir())
    print("Costo equipo (3h con 10% desc):", equipo.calcular_costo(3, descuento=0.10))
    print(asesoria.describir())

    try:
        ServicioInvalido = Asesoria("Mala", -5000, "Redes")
    except ServicioInvalidoError as e: 
        print ("Alarma funciono:", e)   































