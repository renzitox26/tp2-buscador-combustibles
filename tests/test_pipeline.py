
import sys
import unittest
from pathlib import Path

# Permitir importar los archivos de la carpeta src
carpeta_src = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(carpeta_src))

from modelos import ConsultaPrecio
from pipeline import buscar_precios_vigentes


# Fuente de datos ficticia para realizar las pruebas
# No necesitamos utilizar el CSV real
class FuentePrueba:

    def leer_datos(self):
        registros = [
            {
                "empresa": "ESTACION A",
                "direccion": "CALLE 100",
                "localidad": "ROSARIO",
                "provincia": "SANTA FE",
                "producto": "Nafta (súper) entre 92 y 95 Ron",
                "tipohorario": "Diurno",
                "precio": "1200",
                "fecha_vigencia": "01/08/2025 10:00",
                "empresabandera": "YPF"
            },
            {
                "empresa": "ESTACION A",
                "direccion": "CALLE 100",
                "localidad": "ROSARIO",
                "provincia": "SANTA FE",
                "producto": "Nafta (súper) entre 92 y 95 Ron",
                "tipohorario": "Diurno",
                "precio": "1250",
                "fecha_vigencia": "10/08/2025 10:00",
                "empresabandera": "YPF"
            },
            {
                "empresa": "ESTACION A",
                "direccion": "CALLE 100",
                "localidad": "ROSARIO",
                "provincia": "SANTA FE",
                "producto": "Nafta (súper) entre 92 y 95 Ron",
                "tipohorario": "Diurno",
                "precio": "1300",
                "fecha_vigencia": "20/08/2025 10:00",
                "empresabandera": "YPF"
            },
            {
                "empresa": "ESTACION B",
                "direccion": "CALLE 200",
                "localidad": "ROSARIO",
                "provincia": "SANTA FE",
                "producto": "Nafta (súper) entre 92 y 95 Ron",
                "tipohorario": "Diurno",
                "precio": "1100",
                "fecha_vigencia": "12/08/2025 10:00",
                "empresabandera": "SHELL"
            }
        ]

        for registro in registros:
            yield registro


class TestBuscador(unittest.TestCase):

    # PRUEBA 1:
    # Verificar que se seleccione el precio histórico correcto
    def test_precio_historico(self):
        consulta = ConsultaPrecio(
            "Santa Fe",
            "Rosario",
            "Nafta (súper) entre 92 y 95 Ron",
            "Diurno",
            "15/08/2025"
        )

        resultados = buscar_precios_vigentes(
            FuentePrueba(),
            consulta
        )

        # Deben encontrarse dos estaciones
        self.assertEqual(len(resultados), 2)

        # La estación más barata debe aparecer primero
        self.assertEqual(
            resultados[0]["empresa"],
            "ESTACION B"
        )

        self.assertEqual(
            resultados[1]["empresa"],
            "ESTACION A"
        )

        # El precio de la estación A debe ser $1250
        # No debe utilizar el precio posterior de $1300
        self.assertEqual(
            resultados[1]["precio"],
            1250
        )

    # PRUEBA 2:
    # Verificar que no se mezclen provincias
    def test_provincia_sin_resultados(self):
        consulta = ConsultaPrecio(
            "Buenos Aires",
            "Rosario",
            "Nafta (súper) entre 92 y 95 Ron",
            "Diurno",
            "15/08/2025"
        )

        resultados = buscar_precios_vigentes(
            FuentePrueba(),
            consulta
        )

        # No debe encontrar estaciones
        self.assertEqual(len(resultados), 0)

    # PRUEBA 3:
    # Verificar que no se mezclen horarios
    def test_horario_sin_resultados(self):
        consulta = ConsultaPrecio(
            "Santa Fe",
            "Rosario",
            "Nafta (súper) entre 92 y 95 Ron",
            "Nocturno",
            "15/08/2025"
        )

        resultados = buscar_precios_vigentes(
            FuentePrueba(),
            consulta
        )

        # Los registros son diurnos, no nocturnos
        self.assertEqual(len(resultados), 0)

    # PRUEBA 4:
    # Verificar que no se utilicen precios futuros
    def test_fecha_anterior_a_los_registros(self):
        consulta = ConsultaPrecio(
            "Santa Fe",
            "Rosario",
            "Nafta (súper) entre 92 y 95 Ron",
            "Diurno",
            "01/07/2025"
        )

        resultados = buscar_precios_vigentes(
            FuentePrueba(),
            consulta
        )

        # Todos los precios son posteriores a esta fecha
        self.assertEqual(len(resultados), 0)


if __name__ == "__main__":
    unittest.main()
