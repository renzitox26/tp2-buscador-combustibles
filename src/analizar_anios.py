
import csv
from collections import Counter
from pathlib import Path
from datetime import datetime

archivo = Path("data/combustibles_sf_ba.csv")

conteo = Counter()
fechas_invalidas = 0

with open(archivo, "r", encoding="utf-8-sig", newline="") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        try:
            fecha = datetime.strptime(
                fila["fecha_vigencia"].strip(),
                "%d/%m/%Y %H:%M"
            )

            conteo[fecha.year] += 1

        except ValueError:
            fechas_invalidas += 1

print("\nREGISTROS POR AÑO")
print("-------------------------")

for anio in sorted(conteo):
    print(f"{anio}: {conteo[anio]:,}")

print("-------------------------")
print(f"Fechas inválidas: {fechas_invalidas:,}")
print(f"Total analizado: {sum(conteo.values()) + fechas_invalidas:,}")
