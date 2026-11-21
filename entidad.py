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
        return self._id

    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad. Cada subclase la implementa."""
        pass

    def __str__(self):
        return self.describir()
