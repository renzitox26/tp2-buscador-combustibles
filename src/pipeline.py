
from datetime import timedelta
from decimal import Decimal


def buscar_precios_vigentes(fuente, consulta):
    # Incluimos todo el día consultado, hasta las 23:59:59
    limite = consulta.fecha + timedelta(days=1)

    # Guardaremos el registro más reciente de cada estación
    mejores_registros = {}

    for fila in fuente.leer_datos():

        # Filtrar provincia
        if fila["provincia"].strip().upper() != consulta.provincia:
            continue

        # Filtrar localidad
        if fila["localidad"].strip().upper() != consulta.localidad:
            continue

        # Filtrar combustible
        if fila["producto"].strip().lower() != consulta.producto:
            continue

        # Filtrar horario
        if fila["tipohorario"].strip().lower() != consulta.horario:
            continue

        # Convertir la fecha del registro
        from datetime import datetime

        try:
            fecha_registro = datetime.strptime(
                fila["fecha_vigencia"].strip(),
                "%d/%m/%Y %H:%M"
            )
        except ValueError:
            continue

        # No utilizar actualizaciones posteriores a la consulta
        if fecha_registro >= limite:
            continue

        # Identificar provisionalmente la estación
        clave_estacion = (
            fila["empresa"].strip().upper(),
            fila["direccion"].strip().upper(),
            fila["localidad"].strip().upper(),
            fila["provincia"].strip().upper(),
        )

        # Guardar solo el registro más reciente de esa estación
        anterior = mejores_registros.get(clave_estacion)

        if anterior is None or fecha_registro > anterior["fecha"]:
            mejores_registros[clave_estacion] = {
                "empresa": fila["empresa"],
                "direccion": fila["direccion"],
                "localidad": fila["localidad"],
                "provincia": fila["provincia"],
                "bandera": fila["empresabandera"],
                "producto": fila["producto"],
                "horario": fila["tipohorario"],
                "precio": Decimal(
                    fila["precio"].strip().replace(",", ".")
                ),
                "fecha": fecha_registro,
            }

    # Ordenar las estaciones desde el precio más barato
    resultados = list(mejores_registros.values())

    resultados.sort(key=lambda registro: registro["precio"])

    return resultados
