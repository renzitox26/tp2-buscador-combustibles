
from datetime import datetime


class ConsultaPrecio:
    def __init__(
        self,
        provincia,
        localidad,
        producto,
        horario,
        fecha
    ):
        self.provincia = provincia.strip().upper()
        self.localidad = localidad.strip().upper()
        self.producto = producto.strip().lower()
        self.horario = horario.strip().lower()

        self.fecha = datetime.strptime(
            fecha,
            "%d/%m/%Y"
        )

    def mostrar_consulta(self):
        print("\nDATOS DE LA CONSULTA")
        print("-----------------------------")
        print(f"Provincia: {self.provincia}")
        print(f"Localidad: {self.localidad}")
        print(f"Combustible: {self.producto}")
        print(f"Horario: {self.horario}")
        print(f"Fecha: {self.fecha.strftime('%d/%m/%Y')}")
