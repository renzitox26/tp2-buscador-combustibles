
from pathlib import Path

from modelos import ConsultaPrecio
from fuentes import FuenteCSV, FuenteJSON
from pipeline import buscar_precios_vigentes


def elegir_opcion(titulo, opciones):
    print(f"\n{titulo}")
    print("----------------------------------------")

    for numero, opcion in enumerate(opciones, start=1):
        print(f"{numero}. {opcion}")

    while True:
        respuesta = input(
            f"\nElegí una opción (1 al {len(opciones)}): "
        ).strip()

        if respuesta.isdigit():
            numero = int(respuesta)

            if 1 <= numero <= len(opciones):
                return numero - 1

        print("Opción inválida. Intentá nuevamente.")


def obtener_opciones(fuente):
    localidades_por_provincia = {}
    productos = set()

    for fila in fuente.leer_datos():
        provincia = fila["provincia"].strip().upper()
        localidad = fila["localidad"].strip().upper()
        producto = fila["producto"].strip()

        if provincia and localidad:
            localidades_por_provincia.setdefault(
                provincia, set()
            ).add(localidad)

        if producto:
            productos.add(producto)

    return localidades_por_provincia, sorted(productos)


def buscar_localidad(localidades):
    while True:
        texto = input(
            "\nEscribí parte del nombre de la localidad: "
        ).strip().upper()

        if not texto:
            print("Ingresá al menos una letra.")
            continue

        coincidencias = sorted(
            localidad
            for localidad in localidades
            if texto in localidad
        )

        if not coincidencias:
            print("No se encontraron localidades. Intentá otra vez.")
            continue

        if len(coincidencias) > 20:
            print(
                f"Hay {len(coincidencias)} coincidencias. "
                "Escribí un nombre más específico."
            )
            continue

        indice = elegir_opcion(
            "LOCALIDADES ENCONTRADAS",
            coincidencias
        )

        return coincidencias[indice]


def nombre_combustible(producto):
    nombres = {
        "nafta (súper) entre 92 y 95 ron": "Nafta Súper",
        "nafta (premium) de más de 95 ron": "Nafta Premium",
    }

    return nombres.get(
        producto.strip().lower(),
        producto
    )


def realizar_busqueda(fuente, localidades_por_provincia, productos):
    provincias = sorted(localidades_por_provincia)

    indice = elegir_opcion(
        "PROVINCIAS DISPONIBLES",
        provincias
    )
    provincia = provincias[indice]

    localidades = localidades_por_provincia[provincia]
    localidad = buscar_localidad(localidades)

    nombres_visibles = [
        nombre_combustible(producto)
        for producto in productos
    ]

    indice = elegir_opcion(
        "COMBUSTIBLES DISPONIBLES",
        nombres_visibles
    )
    producto = productos[indice]

    horarios = ["Diurno", "Nocturno"]

    indice = elegir_opcion(
        "HORARIOS DISPONIBLES",
        horarios
    )
    horario = horarios[indice]

    while True:
        fecha = input(
            "\nIngresá la fecha (DD/MM/AAAA): "
        ).strip()

        try:
            consulta = ConsultaPrecio(
                provincia,
                localidad,
                producto,
                horario,
                fecha
            )
            break
        except ValueError:
            print("Fecha inválida. Intentá nuevamente.")

    consulta.mostrar_consulta()

    print("\nBuscando precios...")
    resultados = buscar_precios_vigentes(fuente, consulta)

    print("\nRESULTADOS DE LA BÚSQUEDA")
    print("----------------------------------------")

    if not resultados:
        print("No se encontraron precios para esa consulta.")
        return

    print(f"Estaciones encontradas: {len(resultados)}")

    for numero, estacion in enumerate(resultados[:10], start=1):
        print(f"\n{numero}. {estacion['bandera']}")
        print(f"   Empresa: {estacion['empresa']}")
        print(f"   Dirección: {estacion['direccion']}")
        print(f"   Precio: ${estacion['precio']:.2f}")

        print(
            "   Última actualización: "
            f"{estacion['fecha'].strftime('%d/%m/%Y %H:%M')}"
        )

        dias_sin_actualizacion = (
            consulta.fecha.date() - estacion["fecha"].date()
        ).days

        if dias_sin_actualizacion > 90:
            print(
                "   ADVERTENCIA: Precio sin actualizar "
                f"desde hace {dias_sin_actualizacion} días."
            )

    print("\nIMPORTANTE:")
    print("Estos son los últimos precios históricos registrados.")
    print("No se garantiza que fueran los cobrados ese día.")


def main():
    print("========================================")
    print(" BUSCADOR DE PRECIOS DE COMBUSTIBLES")
    print("========================================")

    carpeta_proyecto = Path(__file__).resolve().parent.parent
    carpeta_datos = carpeta_proyecto / "data"

    opciones_fuente = [
        "CSV - Dataset histórico completo",
        "CSV - Muestra de 1000 registros",
        "JSON - Datos de ejemplo"
    ]

    indice = elegir_opcion(
        "SELECCIONAR FUENTE DE DATOS",
        opciones_fuente
    )

    if indice == 0:
        ruta = carpeta_datos / "combustibles_final.csv"
        fuente = FuenteCSV(ruta)

    elif indice == 1:
        ruta = carpeta_datos / "combustibles_muestra.csv"
        fuente = FuenteCSV(ruta)

    else:
        ruta = carpeta_datos / "combustibles_ejemplo.json"
        fuente = FuenteJSON(ruta)

    if not ruta.exists():
        print(f"\nERROR: No se encontró el archivo {ruta.name}")
        print("Probá con otra fuente de datos disponible.")
        return

    print("\nCargando datos...")

    try:
        localidades_por_provincia, productos = obtener_opciones(fuente)
    except (OSError, ValueError) as error:
        print(f"ERROR al leer los datos: {error}")
        return

    if not localidades_por_provincia or not productos:
        print("ERROR: No hay opciones disponibles.")
        return

    while True:
        realizar_busqueda(
            fuente,
            localidades_por_provincia,
            productos
        )

        indice = elegir_opcion(
            "¿QUERÉS REALIZAR OTRA BÚSQUEDA?",
            [
                "Sí, realizar otra búsqueda",
                "No, salir del programa"
            ]
        )

        if indice == 1:
            print("\nGracias por utilizar el buscador.")
            break


if __name__ == "__main__":
    main()
