"""Servicios especializados para Software FJ."""
import logging #vamos a importar la libreria para registrar eventos y errores
from abc import abstractmethod # Sirve para crear las clases con reglas especificas
from entidad import Entidad #traemos el archivo que creo Fabian
from excepciones import ServicioInvalidoError, CalculoInconsistenteError #traemos el archivo que creo Fabian y traigo las clases


#vamos con un logger con el nombre de la empresa 
logger = logging.getLogger("Software FJ")


class Servicio(Entidad):
    """Clase abstracta base para todos los servicios"""

    _contador_id = 0 # Contador para asignar identificadores de cada servicio

    def __init__(self, nombre, tarifa_hora, disponible=True):

        """Parámetros básicos"""
        Servicio.contador_id +=1 #incrementa el contador de los servicios
        super().__init__(Servicio._contador_id) 

        #validamos que el nombre sea letras, y eliminamos los espacios al principio y al final
        if not isinstance(nombre, str) or not nombre.strip():
            logger.error("Fallo al crear servicio: nombre invalido.")
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacio.")

        self.__nombre = nombre.strip() #guarda el nombre como privado
        self.__tarifa_hora = float (tarifa_hora)#guarda la tarifa como decimal privado
        self.__disponible = bool (disponible) # Guarda el interruptor de disponibilidad del producto
        logger.info(f"Servicio base inicializado: ID        id -        ") #registra el inicio del servicio

    











