"""Clase abstracta base de las entidades generales del sistema."""
from abc import ABC, abstractmethod

class Entidad(ABC):
    """Representa cualquier entidad general del sistema cliente, servicio, etc...."""

    def __init__(self, id_entidad):
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
