"""Pruebas automatizadas de servicios, reservas y simulación."""
import contextlib
import io
import math
import unittest

from cliente import Cliente
from excepciones import (
    CalculoInconsistenteError,
    ClienteInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from main import main
from reserva import EstadoReserva, Reserva
from servicios import AlquilerEquipo, Asesoria, ReservaSala, Servicio


class PruebasDeServicios(unittest.TestCase):
    """Comprueba validaciones, polimorfismo y cálculos de servicios."""

    def setUp(self):
        self.sala = ReservaSala("Sala de pruebas", 100, 8)

    def test_calculo_con_parametros_opcionales(self):
        """El cálculo acepta las variantes con impuesto y descuento."""
        self.assertEqual(self.sala.calcular_costo(2), 238.0)
        self.assertEqual(self.sala.calcular_costo(2, 0.1), 220.0)
        self.assertEqual(
            self.sala.calcular_costo(2, impuesto=0.1, descuento=0.25),
            165.0,
        )

    def test_servicios_sobrescriben_calculo_y_descripcion(self):
        """Cada servicio especializado ofrece sus métodos polimórficos."""
        servicios = (
            self.sala,
            AlquilerEquipo("Computador", 200, "Portátil"),
            Asesoria("Asesoría", 300, "Redes"),
        )
        for servicio in servicios:
            with self.subTest(servicio=type(servicio).__name__):
                self.assertIsNot(type(servicio).calcular_costo, Servicio.calcular_costo)
                self.assertIsNot(type(servicio).describir, Servicio.describir)
                self.assertIn(servicio.nombre, servicio.describir())
                self.assertEqual(servicio.calcular_costo(1), servicio.tarifa_hora * 1.19)

    def test_rechaza_parametros_invalidos_de_servicios(self):
        """Tarifas, disponibilidad, capacidad y tipos deben ser válidos."""
        for tarifa in (0, -1, True, math.inf, math.nan, 10**400, "100"):
            with self.subTest(tarifa=tarifa):
                with self.assertRaises(ServicioInvalidoError):
                    ReservaSala("Sala", tarifa, 5)

        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("Sala", 100, True)
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("Sala", 100, 5, disponible="sí")
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo("Equipo", 100, "")
        with self.assertRaises(ServicioInvalidoError):
            Asesoria("Asesoría", 100, " ")
        for crear_servicio in (ReservaSala, AlquilerEquipo, Asesoria):
            with self.subTest(servicio=crear_servicio.__name__):
                with self.assertRaises(ServicioInvalidoError):
                    crear_servicio()
        with self.assertRaises(CalculoInconsistenteError):
            self.sala.calcular_costo()

    def test_rechaza_datos_invalidos_en_calculo_y_disponibilidad(self):
        """Los cálculos y cambios de disponibilidad no aceptan valores ambiguos."""
        for horas in (0, -1, True, math.inf, math.nan, 10**400, "2"):
            with self.subTest(horas=horas):
                with self.assertRaises(CalculoInconsistenteError):
                    self.sala.calcular_costo(horas)

        for impuesto in (-0.1, True, math.inf, "0.1"):
            with self.subTest(impuesto=impuesto):
                with self.assertRaises(CalculoInconsistenteError):
                    self.sala.calcular_costo(1, impuesto=impuesto)

        for descuento in (-0.1, 1.1, True, math.nan, "0.1"):
            with self.subTest(descuento=descuento):
                with self.assertRaises(CalculoInconsistenteError):
                    self.sala.calcular_costo(1, descuento=descuento)

        with self.assertRaises(ServicioInvalidoError):
            self.sala.disponible = "no"

        servicio_grande = ReservaSala("Sala grande", 1e308, 1)
        with self.assertRaises(CalculoInconsistenteError):
            servicio_grande.calcular_costo(2)


class PruebasDeReservas(unittest.TestCase):
    """Comprueba creación, asociación y cambios de estado de las reservas."""

    def setUp(self):
        self.cliente = Cliente("Ana Pérez", "12345678", "ana@example.com", "3001234567")
        self.servicio = ReservaSala("Sala de pruebas", 100, 8)

    def test_reserva_se_asocia_y_se_procesa(self):
        """Una reserva confirmada se procesa y conserva el costo calculado."""
        reserva = Reserva(self.cliente, self.servicio, 2)
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)
        self.assertEqual(self.cliente.obtener_reservas(), [reserva])

        reserva.confirmar()
        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertEqual(reserva.procesar(impuesto=0.1, descuento=0.25), 165.0)
        self.assertEqual(reserva.estado, EstadoReserva.COMPLETADA)
        self.assertEqual(reserva.costo_total, 165.0)
        self.assertIn("Completada", reserva.describir())

    def test_reserva_cancelada_no_se_puede_confirmar_ni_procesar(self):
        """La cancelación impide las siguientes operaciones del flujo."""
        reserva = Reserva(self.cliente, self.servicio, 1)
        reserva.cancelar()
        self.assertEqual(reserva.estado, EstadoReserva.CANCELADA)
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.confirmar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_reserva_completada_no_se_puede_cancelar_ni_procesar_de_nuevo(self):
        """Al completar el servicio, se bloquean acciones que alterarían el estado."""
        reserva = Reserva(self.cliente, self.servicio, 1)
        reserva.confirmar()
        reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.procesar()

    def test_error_de_calculo_no_completa_la_reserva(self):
        """Si falla el costo, la reserva sigue confirmada para volver a intentarlo."""
        reserva = Reserva(self.cliente, self.servicio, 1)
        reserva.confirmar()
        with self.assertRaises(CalculoInconsistenteError):
            reserva.procesar(descuento=2)
        self.assertEqual(reserva.estado, EstadoReserva.CONFIRMADA)
        self.assertIsNone(reserva.costo_total)
        self.assertEqual(reserva.procesar(), 119.0)

    def test_rechaza_cliente_servicio_duracion_o_disponibilidad_invalidos(self):
        """Una reserva requiere objetos correctos, horas positivas y servicio disponible."""
        with self.assertRaises(ReservaInvalidaError):
            Reserva(None, self.servicio, 1)
        with self.assertRaises(ReservaInvalidaError):
            Reserva()
        with self.assertRaises(ReservaInvalidaError):
            Reserva(self.cliente, object(), 1)
        for horas in (0, -1, True, math.inf, math.nan, 10**400, "1"):
            with self.subTest(horas=horas):
                with self.assertRaises(ReservaInvalidaError):
                    Reserva(self.cliente, self.servicio, horas)

        servicio_cerrado = Asesoria("Asesoría", 100, "Redes", disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(self.cliente, servicio_cerrado, 1)

    def test_cliente_encadena_la_causa_del_error_de_validacion(self):
        """El error del registro conserva la causa original de la validación."""
        with self.assertRaises(ClienteInvalidoError) as contexto:
            Cliente()
        self.assertIsNotNone(contexto.exception.__cause__)
        self.assertIn("rechazado", str(contexto.exception))

    def test_errores_directos_del_cliente_se_registran(self):
        """También quedan registrados los errores al cambiar datos o reservas."""
        with self.assertLogs("SoftwareFJ", level="ERROR") as registros:
            with self.assertRaises(ClienteInvalidoError):
                self.cliente.nombre = " "
            with self.assertRaises(ClienteInvalidoError):
                self.cliente.agregar_reserva()

        self.assertEqual(len(registros.records), 2)

    def test_creacion_segura_recupera_datos_omitidos(self):
        """El registro seguro informa el dato faltante y devuelve None."""
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            cliente = Cliente.crear_seguro()
        self.assertIsNone(cliente)
        self.assertIn("[ERROR]", salida.getvalue())

    def test_disponibilidad_se_verifica_al_confirmar(self):
        """Un servicio que deja de estar disponible no permite confirmar la reserva."""
        reserva = Reserva(self.cliente, self.servicio, 1)
        self.servicio.disponible = False
        with self.assertRaises(ServicioNoDisponibleError):
            reserva.confirmar()
        self.assertEqual(reserva.estado, EstadoReserva.PENDIENTE)


class PruebasDeSimulacion(unittest.TestCase):
    """Comprueba que los errores de los ejemplos no detienen el programa."""

    def test_simulacion_ejecuta_mas_de_diez_operaciones(self):
        """La demostración sigue tras los registros y reservas inválidos."""
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            operaciones = main()

        texto = salida.getvalue()
        self.assertGreaterEqual(len(operaciones), 10)
        self.assertIn("Simulación finalizada:", texto)
        self.assertIn("[ERROR]", texto)
        self.assertIn("Intentar reservar servicio no disponible", texto)
        self.assertIn("Intentar reservar duración inválida", texto)


if __name__ == "__main__":
    unittest.main()
