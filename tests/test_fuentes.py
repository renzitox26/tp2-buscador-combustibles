
import sys
import json
import unittest
import tempfile

from pathlib import Path

carpeta_src = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(carpeta_src))

from fuentes import FuenteCSV, FuenteJSON


class TestFuentes(unittest.TestCase):

    def test_fuente_json(self):
        registros = [
            {
                "provincia": "SANTA FE",
                "localidad": "ROSARIO",
                "precio": "1350"
            }
        ]

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "prueba.json"

            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(registros, archivo)

            fuente = FuenteJSON(ruta)
            resultados = list(fuente.leer_datos())

            self.assertEqual(len(resultados), 1)
            self.assertEqual(
                resultados[0]["localidad"],
                "ROSARIO"
            )

    def test_fuente_csv(self):
        contenido = (
            "provincia,localidad,precio\n"
            "SANTA FE,ROSARIO,1350\n"
        )

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "prueba.csv"

            ruta.write_text(contenido, encoding="utf-8")

            fuente = FuenteCSV(ruta)
            resultados = list(fuente.leer_datos())

            self.assertEqual(len(resultados), 1)
            self.assertEqual(
                resultados[0]["precio"],
                "1350"
            )


if __name__ == "__main__":
    unittest.main()
