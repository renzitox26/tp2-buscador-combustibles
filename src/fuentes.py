
import csv
import json

from abc import ABC, abstractmethod
from pathlib import Path


# Clase abstracta: define cómo deben leerse los datos
class FuenteDatos(ABC):

    @abstractmethod
    def leer_datos(self):
        pass


# Clase para leer archivos CSV
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


# Clase para leer archivos JSON
class FuenteJSON(FuenteDatos):

    def __init__(self, ruta_archivo):
        self.ruta_archivo = Path(ruta_archivo)

    def leer_datos(self):
        with open(
            self.ruta_archivo,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError(
                    "El archivo JSON debe contener una lista de registros."
                )

            for registro in datos:
                if not isinstance(registro, dict):
                    raise ValueError(
                        "Cada registro del JSON debe ser un objeto."
                    )

                yield registro
