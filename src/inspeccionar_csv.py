
import csv
from pathlib import Path

# Buscar los archivos CSV dentro de data/
carpeta_datos = Path("data")
archivos = list(carpeta_datos.glob("*.csv"))

if not archivos:
    print("No se encontró ningún archivo CSV.")
else:
    archivo = archivos[0]

    print(f"Archivo encontrado: {archivo.name}")

    with open(archivo, "r", encoding="utf-8-sig", newline="") as f:
        muestra = f.read(8192)
        f.seek(0)

        # Detectar el separador del CSV
        separador = csv.Sniffer().sniff(muestra, delimiters=",;").delimiter

        lector = csv.reader(f, delimiter=separador)

        columnas = next(lector)

        print("\nCOLUMNAS DEL DATASET:")
        for numero, columna in enumerate(columnas, start=1):
            print(f"{numero}. {columna}")

        print("\nPRIMERAS 3 FILAS:")
        for _, fila in zip(range(3), lector):
            print(fila)
