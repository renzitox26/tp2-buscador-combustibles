
from datetime import datetime

from validaciones import normalizar_texto, validar_formato_fecha


class ConsultaPrecio:

    def __init__(self, provincia, localidad, producto, horario, fecha):

        self.provincia = normalizar_texto(provincia).upper()
        self.localidad = normalizar_texto(localidad).upper()
        self.producto = normalizar_texto(producto).lower()
        self.horario = normalizar_texto(horario).lower()

        fecha = normalizar_texto(fecha)

        if not validar_formato_fecha(fecha):
            raise ValueError(
                "La fecha debe tener el formato DD/MM/AAAA "
                "y ser una fecha válida."
            )

        self.fecha = datetime.strptime(fecha, "%d/%m/%Y")

    def mostrar_consulta(self):
        print("\nDATOS DE LA CONSULTA")
        print("-----------------------------")
        print(f"Provincia: {self.provincia}")
        print(f"Localidad: {self.localidad}")
        print(f"Combustible: {self.producto}")
        print(f"Horario: {self.horario}")
        print(f"Fecha: {self.fecha.strftime('%d/%m/%Y')}")
