
import re
from datetime import datetime


def normalizar_texto(texto):
    """
    Elimina espacios al principio y al final,
    y reemplaza espacios repetidos por uno solo.
    """
    if not isinstance(texto, str):
        return ""

    texto = texto.strip()
    texto = re.sub(r"\s+", " ", texto)

    return texto


def validar_formato_fecha(fecha):
    """
    Verifica que la fecha tenga formato DD/MM/AAAA
    y que sea una fecha real.
    """
    if not isinstance(fecha, str):
        return False

    patron = r"\d{2}/\d{2}/\d{4}"

    if not re.fullmatch(patron, fecha):
        return False

    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_formato_fecha_hora(fecha):
    """
    Verifica que la fecha y hora tengan
    formato DD/MM/AAAA HH:MM.
    """
    if not isinstance(fecha, str):
        return False

    patron = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"

    if not re.fullmatch(patron, fecha):
        return False

    try:
        datetime.strptime(fecha, "%d/%m/%Y %H:%M")
        return True
    except ValueError:
        return False
