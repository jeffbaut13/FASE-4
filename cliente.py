"""Clase Cliente del sistema Software FJ."""
import re
import logging

from entidad import Entidad
from excepciones import ClienteInvalidoError

logger = logging.getLogger("SoftwareFJ")


class Cliente(Entidad):
    """Representa a un cliente de Software FJ.

    Los datos personales son privados y solo se
    acceden o modifican mediante propiedades con validación estricta.
    """

    _contador_id = 0  # Genera identificadores únicos automáticamente

    def __init__(self, nombre, documento, correo, telefono):
        try:
            self.__nombre = None
            self.__documento = None
            self.__correo = None
            self.__telefono = None

            self.nombre = nombre
            self.documento = documento
            self.correo = correo
            self.telefono = telefono
        except ClienteInvalidoError as error:
            logger.error("No se pudo crear el cliente: %s", error)
            raise ClienteInvalidoError(
                "Registro de cliente rechazado por datos inválidos"
            ) from error  # Encadenamiento de excepciones

        Cliente._contador_id += 1
        self.__id_cliente = Cliente._contador_id
        super().__init__(self.__id_cliente)
        self.__reservas = []  # Lista interna de reservas del cliente
        logger.info("Cliente creado: ID %s - %s", self.__id_cliente, self.__nombre)

    # ########Propiedades###########
    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or not isinstance(valor, str):
            raise ClienteInvalidoError("El nombre es obligatorio y debe ser texto")
        valor = valor.strip()
        if len(valor) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+", valor):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios")
        self.__nombre = valor.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None:
            raise ClienteInvalidoError("El documento es obligatorio")
        valor = str(valor).strip()
        if not valor.isdigit() or not (6 <= len(valor) <= 12):
            raise ClienteInvalidoError(
                "El documento debe ser numérico y tener entre 6 y 12 dígitos"
            )
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or not isinstance(valor, str):
            raise ClienteInvalidoError("El correo es obligatorio y debe ser texto")
        valor = valor.strip().lower()
        if not re.fullmatch(r"[\w\.\-]+@[\w\-]+(\.[\w\-]+)+", valor):
            raise ClienteInvalidoError(f"Formato de correo inválido: '{valor}'")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise ClienteInvalidoError("El teléfono es obligatorio")
        valor = str(valor).strip().replace(" ", "")
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos")
        self.__telefono = valor

    # Manejo de la lista interna de reservas 
    def agregar_reserva(self, reserva):
        if reserva is None:
            raise ClienteInvalidoError("No se puede asociar una reserva nula")
        self.__reservas.append(reserva)

    def obtener_reservas(self):
        return list(self.__reservas)  ###### Copia y protege la lista interna

    # #####Creación segura (try/except/else/finally) ##########
    @classmethod
    def crear_seguro(cls, nombre, documento, correo, telefono):
        """Intenta crear un cliente sin detener el programa si hay errores."""
        cliente = None
        try:
            cliente = cls(nombre, documento, correo, telefono)
        except ClienteInvalidoError as error:
            logger.error("Fallo en crear_seguro: %s | Causa: %s", error, error.__cause__)
            print(f"[ERROR] {error} -> Causa: {error.__cause__}")
        else:
            print(f"[OK] Cliente registrado: {cliente}")
        finally:
            logger.info("Intento de registro de cliente finalizado")
        return cliente

    # ######## Representaciones #########
    def describir(self):
        return (f"Cliente #{self.__id_cliente} | {self.__nombre} | "
                f"Doc: {self.__documento} | {self.__correo} | Tel: {self.__telefono}")

    def __repr__(self):
        return f"Cliente(id={self.__id_cliente}, nombre='{self.__nombre}')"
