
import csv
from datetime import datetime
from pathlib import Path

ARCHIVO_ENTRADA = Path("data/combustibles_sf_ba.csv")
ARCHIVO_SALIDA = Path("data/combustibles_2024_2026.csv")

total_leidos = 0
total_guardados = 0
fechas_invalidas = 0

conteo_anios = {
    2024: 0,
    2025: 0,
    2026: 0
}

with open(
    ARCHIVO_ENTRADA,
    "r",
    encoding="utf-8-sig",
    newline=""
) as entrada:

    lector = csv.DictReader(entrada)

    with open(
        ARCHIVO_SALIDA,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as salida:

        escritor = csv.DictWriter(
            salida,
            fieldnames=lector.fieldnames
        )

        escritor.writeheader()

        for fila in lector:
            total_leidos += 1

            try:
                fecha = datetime.strptime(
                    fila["fecha_vigencia"].strip(),
                    "%d/%m/%Y %H:%M"
                )

            except ValueError:
                fechas_invalidas += 1
                continue

            if 2024 <= fecha.year <= 2026:
                escritor.writerow(fila)
                total_guardados += 1
                conteo_anios[fecha.year] += 1

print("\nRESULTADO DEL FILTRADO")
print("-----------------------------")
print(f"Registros leídos: {total_leidos:,}")
print(f"Registros conservados: {total_guardados:,}")
print(f"Fechas no interpretables: {fechas_invalidas:,}")

for anio, cantidad in conteo_anios.items():
    print(f"{anio}: {cantidad:,}")

tamano_mb = ARCHIVO_SALIDA.stat().st_size / (1024 * 1024)
print(f"Tamaño del archivo: {tamano_mb:.2f} MB")
print(f"Archivo generado: {ARCHIVO_SALIDA}")
