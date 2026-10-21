
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

ARCHIVO = Path("data/combustibles_2024_2026.csv")

with open(ARCHIVO, "r", encoding="utf-8-sig", newline="") as f:
    lector = csv.DictReader(f)

    for numero, fila in enumerate(lector, start=2):
        precio_texto = fila["precio"].strip()

        motivo = None

        if not precio_texto:
            motivo = "Precio vacío"
        else:
            try:
                precio = Decimal(precio_texto.replace(",", "."))

                if not precio.is_finite():
                    motivo = "Precio no finito"
                elif precio <= 0:
                    motivo = "Precio menor o igual a cero"

            except InvalidOperation:
                motivo = "Precio no numérico"

        if motivo:
            print(f"\nFila del CSV: {numero}")
            print(f"Motivo: {motivo}")
            print(f"Precio original: {precio_texto!r}")
            print(f"Provincia: {fila['provincia']}")
            print(f"Localidad: {fila['localidad']}")
            print(f"Producto: {fila['producto']}")
            print(f"Horario: {fila['tipohorario']}")
            print(f"Fecha: {fila['fecha_vigencia']}")
