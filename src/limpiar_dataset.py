
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

ARCHIVO_ENTRADA = Path("data/combustibles_2024_2026.csv")
ARCHIVO_SALIDA = Path("data/combustibles_final.csv")

total_leidos = 0
precios_invalidos = 0
duplicados = 0
total_guardados = 0

filas_vistas = set()

with open(
    ARCHIVO_ENTRADA,
    "r",
    encoding="utf-8-sig",
    newline=""
) as entrada:

    lector = csv.DictReader(entrada)
    columnas = lector.fieldnames

    with open(
        ARCHIVO_SALIDA,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as salida:

        escritor = csv.DictWriter(
            salida,
            fieldnames=columnas
        )

        escritor.writeheader()

        for fila in lector:
            total_leidos += 1

            # Validar el precio
            precio_texto = fila["precio"].strip()

            try:
                precio = Decimal(precio_texto.replace(",", "."))

                if not precio.is_finite() or precio <= 0:
                    precios_invalidos += 1
                    continue

            except InvalidOperation:
                precios_invalidos += 1
                continue

            # Detectar duplicados exactos
            clave = tuple(fila[columna] for columna in columnas)

            if clave in filas_vistas:
                duplicados += 1
                continue

            filas_vistas.add(clave)

            # Guardar el registro válido
            escritor.writerow(fila)
            total_guardados += 1

print("\nRESULTADO DE LA LIMPIEZA")
print("--------------------------------")
print(f"Registros leídos: {total_leidos:,}")
print(f"Precios inválidos: {precios_invalidos:,}")
print(f"Duplicados eliminados: {duplicados:,}")
print(f"Registros guardados: {total_guardados:,}")

tamano_mb = ARCHIVO_SALIDA.stat().st_size / (1024 * 1024)

print(f"Tamaño final: {tamano_mb:.2f} MB")
print(f"Archivo generado: {ARCHIVO_SALIDA}")
