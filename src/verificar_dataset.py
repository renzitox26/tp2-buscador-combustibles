
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

ARCHIVO = Path("data/combustibles_final.csv")

total = 0
precios_invalidos = 0
duplicados = 0
filas_vistas = set()

with open(ARCHIVO, "r", encoding="utf-8-sig", newline="") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        total += 1

        # Verificar que el precio sea positivo
        try:
            precio = Decimal(fila["precio"].strip().replace(",", "."))

            if not precio.is_finite() or precio <= 0:
                precios_invalidos += 1

        except InvalidOperation:
            precios_invalidos += 1

        # Verificar que no existan duplicados exactos
        clave = tuple(fila.items())

        if clave in filas_vistas:
            duplicados += 1

        filas_vistas.add(clave)

print("\nVERIFICACIÓN DEL DATASET")
print("-------------------------------")
print(f"Registros: {total:,}")
print(f"Precios inválidos: {precios_invalidos}")
print(f"Duplicados exactos: {duplicados}")

if total == 463809 and precios_invalidos == 0 and duplicados == 0:
    print("\nVERIFICACIÓN EXITOSA")
else:
    print("\nATENCIÓN: Revisar los resultados")
