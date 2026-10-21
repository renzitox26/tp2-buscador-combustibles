
import csv
from datetime import datetime
from pathlib import Path

archivo = Path("data/combustibles_sf_ba.csv")

mostrados = 0
total_sospechosos = 0

with open(archivo, "r", encoding="utf-8-sig", newline="") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        fecha_texto = fila["fecha_vigencia"].strip()

        try:
            fecha = datetime.strptime(
                fecha_texto,
                "%d/%m/%Y %H:%M"
            )

            if fecha.year < 2016 or fecha.year > 2026:
                total_sospechosos += 1

                if mostrados < 15:
                    print(
                        f"Fecha: {fecha_texto!r} | "
                        f"Provincia: {fila['provincia']} | "
                        f"Producto: {fila['producto']}"
                    )
                    mostrados += 1

        except ValueError:
            total_sospechosos += 1

            if mostrados < 15:
                print(f"Fecha no interpretable: {fecha_texto!r}")
                mostrados += 1

print(f"\nTotal de fechas sospechosas: {total_sospechosos:,}")
