"""Define la clase Cliente y las reglas para registrar sus datos personales."""
import re
import logging

from entidad import Entidad
from excepciones import ClienteInvalidoError

logger = logging.getLogger("SoftwareFJ")


class Cliente(Entidad):
    """Representa a una persona registrada en el sistema Software FJ.

    Sus datos se guardan como atributos privados y se validan mediante
    propiedades para evitar registrar valores con formatos incorrectos.
    """

    # Este contador compartido asigna un número consecutivo a cada cliente.
    _contador_id = 0

    def __init__(self, nombre, documento, correo, telefono):
        """Crea un cliente, valida sus datos y le asigna un identificador.

        Los parámetros son los datos personales que se guardarán en el objeto.
        Si alguna validación falla, se registra el error y no se completa el alta.
        """
        try:
            # Se inicializan los atributos antes de usar sus propiedades validadoras.
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
        # Cada cliente mantiene su propia lista de reservas asociadas.
        self.__reservas = []
        logger.info("Cliente creado: ID %s - %s", self.__id_cliente, self.__nombre)

    @property
    def id_cliente(self):
        """Devuelve el identificador consecutivo del cliente."""
        return self.__id_cliente

    @property
    def nombre(self):
        """Devuelve el nombre que ya fue validado al guardarse."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida el nombre y lo guarda con formato de título."""
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
        """Devuelve el documento guardado como texto."""
        return self.__documento

    @documento.setter
    def documento(self, valor):
        """Comprueba que el documento tenga entre 6 y 12 dígitos."""
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
        """Devuelve la dirección de correo en minúsculas."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        """Valida el formato del correo antes de guardarlo."""
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
