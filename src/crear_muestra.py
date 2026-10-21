
import csv
import random
from pathlib import Path


def crear_muestra():
    carpeta_proyecto = Path(__file__).resolve().parent.parent

    archivo_original = (
        carpeta_proyecto / "data" / "combustibles_final.csv"
    )

    archivo_muestra = (
        carpeta_proyecto / "data" / "combustibles_muestra.csv"
    )

    cantidad_muestra = 1000
    generador = random.Random(42)

    muestra = []

    with open(
        archivo_original,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo)
        columnas = lector.fieldnames

        for numero, fila in enumerate(lector, start=1):

            if len(muestra) < cantidad_muestra:
                muestra.append(fila)

            else:
                posicion = generador.randint(1, numero)

                if posicion <= cantidad_muestra:
                    muestra[posicion - 1] = fila

    with open(
        archivo_muestra,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        escritor.writeheader()
        escritor.writerows(muestra)

    print("Muestra creada correctamente.")
    print(f"Registros guardados: {len(muestra)}")
    print(f"Archivo: {archivo_muestra}")


if __name__ == "__main__":
    crear_muestra()
