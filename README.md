
# Buscador Histórico de Precios de Combustibles

## Descripción

Este proyecto fue desarrollado en Python para consultar precios
históricos de combustibles en estaciones de servicio de Argentina.

Permite realizar búsquedas por provincia, localidad, tipo de
combustible, horario y fecha.

El programa utiliza registros históricos de estaciones de servicio
de las provincias de Santa Fe y Buenos Aires, correspondientes
al período 2024-2026.

## Funcionalidades

- Selección de provincia mediante un menú.
- Búsqueda de localidades por nombre.
- Selección del tipo de combustible.
- Selección de horario diurno o nocturno.
- Consulta de precios históricos por fecha.
- Identificación de la última actualización disponible por estación.
- Ordenamiento de estaciones por precio.
- Advertencias cuando un precio tiene más de 90 días de antigüedad.
- Posibilidad de realizar múltiples consultas.
- Lectura de archivos CSV y JSON.
- Pruebas automáticas.

## Tecnologías utilizadas

- Python 3
- Programación orientada a objetos
- Módulos estándar: csv, json, datetime, pathlib, decimal y unittest
- Git y GitHub

## Estructura del proyecto

```text
tp2-buscador-combustibles/
|
|-- data/
|   |-- combustibles_muestra.csv
|   |-- combustibles_ejemplo.json
|
|-- src/
|   |-- main.py
|   |-- modelos.py
|   |-- fuentes.py
|   |-- pipeline.py
|   |-- crear_muestra.py
|   |-- otros scripts de preparación de datos
|
|-- tests/
|   |-- test_pipeline.py
|   |-- test_fuentes.py
|
|-- outputs/
|-- .gitignore
|-- requirements.txt
|-- README.md
```

## Instalación

1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto en Visual Studio Code.
3. Tener instalado Python 3.
4. Abrir una terminal en la carpeta principal.

El programa utiliza únicamente módulos de la biblioteca estándar
de Python, por lo que no requiere instalar paquetes externos.

## Ejecución

Ejecutar:

    python src/main.py

Al iniciar, el programa permite elegir una fuente de datos:

1. CSV: dataset histórico completo.
2. CSV: muestra de 1.000 registros.
3. JSON: datos ficticios de ejemplo.

La muestra CSV y el JSON de ejemplo están incluidos en el repositorio.

El dataset completo no se incluye debido a su tamaño.

## Ejemplo de consulta

- Provincia: Santa Fe
- Localidad: Rosario
- Combustible: Nafta Súper
- Horario: Diurno
- Fecha: 15/08/2025

El programa devuelve las estaciones encontradas, sus precios
históricos y la fecha de la última actualización registrada.

## Pruebas automáticas

Para ejecutar las pruebas:

    python -m unittest discover -s tests -v

Las pruebas comprueban:

- Selección correcta del precio histórico.
- Exclusión de registros posteriores a la fecha consultada.
- Filtrado por provincia.
- Filtrado por horario.
- Consultas sin resultados.
- Lectura de archivos CSV.
- Lectura de archivos JSON.

## Diseño orientado a objetos

El proyecto utiliza las siguientes clases:

- FuenteDatos: clase abstracta que define el método leer_datos().
- FuenteCSV: implementación para leer archivos CSV.
- FuenteJSON: implementación para leer archivos JSON.
- ConsultaPrecio: representa los parámetros de una consulta.

La función buscar_precios_vigentes() procesa los registros
y selecciona la última actualización disponible de cada estación.

## Preparación y limpieza de datos

El dataset original fue procesado para:

- Seleccionar las columnas necesarias.
- Filtrar las provincias Santa Fe y Buenos Aires.
- Limitar los registros al período 2024-2026.
- Eliminar precios inválidos o iguales a cero.
- Eliminar registros exactamente duplicados.
- Generar un archivo final de consulta.
- Crear una muestra reproducible de 1.000 registros.

## Limitaciones

Los resultados corresponden a registros históricos declarados.

La última actualización registrada no garantiza que el precio
haya sido efectivamente cobrado en la fecha consultada.

Los precios con más de 90 días desde su última actualización
se muestran con una advertencia.

La muestra de 1.000 registros no representa necesariamente
todas las estaciones, localidades o fechas.

El archivo JSON incluido contiene datos ficticios y se utiliza
únicamente para demostrar el funcionamiento de FuenteJSON.
