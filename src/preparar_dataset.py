
import csv
from pathlib import Path

# Carpeta donde guardamos los datos
CARPETA_DATOS = Path("data")

# Columnas que queremos conservar
COLUMNAS = [
    "empresa",
    "direccion",
    "localidad",
    "provincia",
    "producto",
    "tipohorario",
    "precio",
    "fecha_vigencia",
    "empresabandera",
]


def preparar_dataset():

    # Buscar el archivo CSV original
    archivos = [
        archivo
        for archivo in CARPETA_DATOS.glob("*.csv")
        if archivo.name != "combustibles_limpio.csv"
    ]

    if len(archivos) != 1:
        print("ERROR: Debe existir un único CSV original en data/")
        return

    archivo_original = archivos[0]
    archivo_salida = CARPETA_DATOS / "combustibles_limpio.csv"

    total_filas = 0

    # Abrir el archivo original
    with open(
        archivo_original,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as entrada:

        # Detectar el separador
        muestra = entrada.read(8192)
        entrada.seek(0)

        separador = csv.Sniffer().sniff(
            muestra,
            delimiters=",;"
        ).delimiter

        lector = csv.DictReader(
            entrada,
            delimiter=separador
        )

        # Comprobar las columnas
        faltantes = [
            columna
            for columna in COLUMNAS
            if columna not in lector.fieldnames
        ]

        if faltantes:
            print("ERROR: Faltan columnas:", faltantes)
            return

        # Crear el CSV reducido
        with open(
            archivo_salida,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as salida:

            escritor = csv.DictWriter(
                salida,
                fieldnames=COLUMNAS
            )

            escritor.writeheader()

            for fila in lector:

                fila_reducida = {
                    columna: fila[columna]
                    for columna in COLUMNAS
                }

                escritor.writerow(fila_reducida)
                total_filas += 1

    print("Proceso finalizado correctamente.")
    print(f"Filas procesadas: {total_filas}")
    print(f"Archivo generado: {archivo_salida}")


if __name__ == "__main__":
    preparar_dataset()
