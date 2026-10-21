
import sys
import unittest

from pathlib import Path
from decimal import Decimal

carpeta_src = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(carpeta_src))

from modelos import ConsultaPrecio
from pipeline import buscar_precios_vigentes


class FuentePrueba:

    def __init__(self, registros):
        self.registros = registros

    def leer_datos(self):
        for registro in self.registros:
            yield registro


class TestValidaciones(unittest.TestCase):

    def setUp(self):
        self.registro_valido = {
            "empresa": "ESTACION A",
            "direccion": "CALLE 123",
            "localidad": "ROSARIO",
            "provincia": "SANTA FE",
            "producto": "Nafta (súper) entre 92 y 95 Ron",
            "tipohorario": "Diurno",
            "precio": "1250",
            "fecha_vigencia": "10/08/2025 10:00",
            "empresabandera": "YPF"
        }

        self.consulta = ConsultaPrecio(
            "Santa Fe",
            "Rosario",
            "Nafta (súper) entre 92 y 95 Ron",
            "Diurno",
            "15/08/2025"
        )

    def crear_registro(self, **cambios):
        registro = self.registro_valido.copy()
        registro.update(cambios)
        return registro

    def buscar(self, registros):
        fuente = FuentePrueba(registros)

        return buscar_precios_vigentes(
            fuente,
            self.consulta
        )

    def test_precio_no_numerico(self):
        registros = [
            self.crear_registro(precio="ERROR"),
            self.crear_registro()
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 1)
        self.assertEqual(
            resultados[0]["precio"],
            Decimal("1250")
        )

    def test_precio_negativo(self):
        registros = [
            self.crear_registro(precio="-500")
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)

    def test_precio_cero(self):
        registros = [
            self.crear_registro(precio="0")
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)

    def test_fecha_invalida(self):
        registros = [
            self.crear_registro(
                fecha_vigencia="FECHA INCORRECTA"
            )
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)

    def test_direccion_vacia(self):
        registros = [
            self.crear_registro(direccion="")
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)

    def test_campo_obligatorio_faltante(self):
        registro = self.registro_valido.copy()
        del registro["precio"]

        resultados = self.buscar([registro])

        self.assertEqual(len(resultados), 0)

    def test_registro_posterior_a_consulta(self):
        registros = [
            self.crear_registro(
                fecha_vigencia="20/08/2025 10:00"
            )
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)

    def test_precio_con_coma_decimal(self):
        registros = [
            self.crear_registro(precio="1250,50")
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 1)
        self.assertEqual(
            resultados[0]["precio"],
            Decimal("1250.50")
        )

    def test_precio_infinito(self):
        registros = [
            self.crear_registro(precio="Infinity")
        ]

        resultados = self.buscar(registros)

        self.assertEqual(len(resultados), 0)


if __name__ == "__main__":
    unittest.main()
