
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation


def buscar_precios_vigentes(fuente, consulta):
    limite = consulta.fecha + timedelta(days=1)

    mejores_registros = {}

    campos_obligatorios = [
        "provincia",
        "localidad",
        "producto",
        "tipohorario",
        "fecha_vigencia",
        "precio",
        "empresa",
        "direccion",
        "empresabandera"
    ]

    for fila in fuente.leer_datos():

        # 1. Comprobar que estén todos los campos
        if any(
            campo not in fila or fila[campo] is None
            for campo in campos_obligatorios
        ):
            continue

        # 2. Filtrar según la consulta
        if fila["provincia"].strip().upper() != consulta.provincia:
            continue

        if fila["localidad"].strip().upper() != consulta.localidad:
            continue

        if fila["producto"].strip().lower() != consulta.producto:
            continue

        if fila["tipohorario"].strip().lower() != consulta.horario:
            continue

        # 3. Validar fecha
        try:
            fecha_registro = datetime.strptime(
                fila["fecha_vigencia"].strip(),
                "%d/%m/%Y %H:%M"
            )
        except ValueError:
            continue

        # No utilizar precios actualizados después de la fecha buscada
        if fecha_registro >= limite:
            continue

        # 4. Validar precio
        try:
            precio = Decimal(
                fila["precio"].strip().replace(",", ".")
            )
        except (InvalidOperation, ValueError):
            continue

        # Rechazar precios negativos, cero, infinitos y NaN
        if not precio.is_finite() or precio <= 0:
            continue

        # 5. Validar identificación de la estación
        empresa = fila["empresa"].strip()
        direccion = fila["direccion"].strip()

        if not empresa or not direccion:
            continue

        clave_estacion = (
            empresa.upper(),
            direccion.upper(),
            fila["localidad"].strip().upper(),
            fila["provincia"].strip().upper()
        )

        anterior = mejores_registros.get(clave_estacion)

        # 6. Conservar el precio más reciente por estación
        if anterior is None or fecha_registro > anterior["fecha"]:
            mejores_registros[clave_estacion] = {
                "empresa": empresa,
                "direccion": direccion,
                "localidad": fila["localidad"],
                "provincia": fila["provincia"],
                "bandera": fila["empresabandera"],
                "producto": fila["producto"],
                "horario": fila["tipohorario"],
                "precio": precio,
                "fecha": fecha_registro
            }

    # 7. Ordenar de menor a mayor precio
    resultados = list(mejores_registros.values())

    resultados.sort(
        key=lambda registro: registro["precio"]
    )

    return resultados
