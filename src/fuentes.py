
import csv
from abc import ABC, abstractmethod
from pathlib import Path


class FuenteDatos(ABC):
    @abstractmethod
    def leer_datos(self):
        pass


class FuenteCSV(FuenteDatos):
    def __init__(self, ruta_archivo):
        self.ruta_archivo = Path(ruta_archivo)

    def leer_datos(self):
        with open(
            self.ruta_archivo,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as archivo:

            lector = csv.DictReader(archivo)

            for fila in lector:
                yield fila
