
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

ARCHIVO = Path("data/combustibles_2024_2026.csv")

horarios = Counter()
precios_invalidos = 0
precios_vacios = 0
filas_duplicadas = 0
total = 0

filas_vistas = set()

with open(ARCHIVO, "r", encoding="utf-8-sig", newline="") as f:
    lector = csv.DictReader(f)

    columnas = lector.fieldnames

    for fila in lector:
        total += 1

        # Contar los tipos de horario
        horario = fila["tipohorario"].strip()
        horarios[horario] += 1

        # Comprobar los precios
        precio_texto = fila["precio"].strip()

        if not precio_texto:
            precios_vacios += 1
        else:
            try:
                precio = Decimal(precio_texto.replace(",", "."))

                if not precio.is_finite() or precio <= 0:
                    precios_invalidos += 1

            except InvalidOperation:
                precios_invalidos += 1

        # Detectar filas exactamente iguales
        clave = tuple(fila[columna] for columna in columnas)

        if clave in filas_vistas:
            filas_duplicadas += 1
        else:
            filas_vistas.add(clave)

print("\nANÁLISIS DE CALIDAD")
print("-------------------------------")
print(f"Registros analizados: {total:,}")
print(f"Precios vacíos: {precios_vacios:,}")
print(f"Precios inválidos: {precios_invalidos:,}")
print(f"Filas duplicadas exactas: {filas_duplicadas:,}")

print("\nTIPOS DE HORARIO")
print("-------------------------------")

for horario, cantidad in horarios.most_common():
    print(f"{horario!r}: {cantidad:,}")
