
import sys
import unittest
from pathlib import Path

carpeta_src = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(carpeta_src))

from validaciones import (
    normalizar_texto,
    validar_formato_fecha,
    validar_formato_fecha_hora
)


class TestRegex(unittest.TestCase):

    def test_normalizar_espacios(self):
        resultado = normalizar_texto("  SAN   MARTIN   123  ")
        self.assertEqual(resultado, "SAN MARTIN 123")

    def test_normalizar_texto_invalido(self):
        self.assertEqual(normalizar_texto(None), "")

    def test_fecha_correcta(self):
        self.assertTrue(validar_formato_fecha("15/08/2025"))

    def test_fecha_formato_incorrecto(self):
        self.assertFalse(validar_formato_fecha("2025-08-15"))

    def test_fecha_inexistente(self):
        self.assertFalse(validar_formato_fecha("31/02/2025"))

    def test_fecha_hora_correcta(self):
        self.assertTrue(
            validar_formato_fecha_hora("15/08/2025 10:30")
        )

    def test_fecha_hora_incorrecta(self):
        self.assertFalse(
            validar_formato_fecha_hora("15/08/2025 25:90")
        )


if __name__ == "__main__":
    unittest.main()
