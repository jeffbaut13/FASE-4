"""Clase abstracta base de las entidades generales del sistema."""
from abc import ABC, abstractmethod

class Entidad(ABC):
    """Clase común para objetos del sistema que tienen un identificador.

    Es abstracta porque cada entidad concreta debe definir cómo describirse.
    """

    def __init__(self, id_entidad):
        """Guarda el identificador que recibe la entidad hija."""
        self._id = id_entidad

    @property
    def id(self):
        """Devuelve el identificador de esta entidad."""
        return self._id

    @abstractmethod
    def describir(self):
        """Define la descripción que debe implementar cada clase hija."""
        pass

    def __str__(self):
        """Usa la descripción para mostrar la entidad como texto."""
        return self.describir()
