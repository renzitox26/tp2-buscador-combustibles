
import csv
from pathlib import Path

# Archivos de entrada y salida
ARCHIVO_ORIGINAL = Path("data/combustibles_limpio.csv")
ARCHIVO_FILTRADO = Path("data/combustibles_sf_ba.csv")

# Provincias que queremos conservar
PROVINCIAS = {"SANTA FE", "BUENOS AIRES"}

total_leidos = 0
total_guardados = 0
conteo_provincias = {
    "SANTA FE": 0,
    "BUENOS AIRES": 0,
}

with open(
    ARCHIVO_ORIGINAL,
    "r",
    encoding="utf-8-sig",
    newline=""
) as entrada:

    lector = csv.DictReader(entrada)

    with open(
        ARCHIVO_FILTRADO,
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

            provincia = fila["provincia"].strip().upper()

            if provincia in PROVINCIAS:
                escritor.writerow(fila)
                total_guardados += 1
                conteo_provincias[provincia] += 1

print("\nPROCESO FINALIZADO")
print("-----------------------------")
print(f"Registros originales: {total_leidos:,}")
print(f"Registros conservados: {total_guardados:,}")
print(f"Santa Fe: {conteo_provincias['SANTA FE']:,}")
print(f"Buenos Aires: {conteo_provincias['BUENOS AIRES']:,}")

porcentaje = total_guardados / total_leidos * 100
print(f"Porcentaje conservado: {porcentaje:.2f}%")

tamano_mb = ARCHIVO_FILTRADO.stat().st_size / (1024 * 1024)
print(f"Tamaño del nuevo archivo: {tamano_mb:.2f} MB")
print(f"Archivo generado: {ARCHIVO_FILTRADO}")
