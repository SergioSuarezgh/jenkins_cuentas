import polars as pl
from datetime import datetime


def parse_datetime_expr(col: pl.Expr) -> pl.Expr:
    """
    Devuelve una expresión de Polars que intenta convertir una columna a tipo datetime
    probando varios formatos comunes.

    Estrategia:
        1. Si ya es datetime → castea de forma "suave" (no lanza error si falla).
        2. Intenta el formato ISO estándar: ``YYYY-MM-DD HH:MM:SS``.
        3. Intenta el formato europeo con hora: ``DD/MM/YYYY HH:MM:SS``.
        4. Intenta fecha corta ``DD/MM/YYYY`` → se convierte a date y luego a datetime.

    Args:
        col (pl.Expr): Expresión de Polars (columna) a transformar.

    Returns:
        pl.Expr: Expresión que representa la conversión a datetime aplicando
        la primera coincidencia válida.
    """
    return pl.coalesce([
        col.cast(pl.Datetime("ms"), strict=False),
        col.str.to_datetime(format="%Y-%m-%d %H:%M:%S", strict=False),
        col.str.to_datetime(format="%d/%m/%Y %H:%M:%S", strict=False),
        col.str.to_date(format="%d/%m/%Y", strict=False).cast(pl.Datetime("ms")),
    ])


def _parse_fecha_yyyy_mm_dd(value: str) -> datetime:
    """
    Convierte un string con formato ``YYYY-MM-DD`` en un objeto datetime.

    Args:
        value (str): Cadena en formato de fecha ISO corto (ej. ``"2025-01-15"``).

    Returns:
        datetime: Fecha correspondiente al valor proporcionado.
    """
    return datetime.strptime(value, "%Y-%m-%d")


def _fmt_ddmmaa(d: datetime) -> str:
    """
    Formatea un objeto datetime en cadena con el patrón ``ddmmaa``,
    donde el año se muestra con dos dígitos.

    Args:
        d (datetime): Fecha a formatear.

    Returns:
        str: Cadena con formato ``ddmmaa`` (ej. ``150125`` para 15/01/2025).
    """
    return d.strftime("%d%m%y")



