import polars as pl

class Etl:
    def __init__(self, fichero, fila_cabecera):
        self.fichero = fichero
        self.fila_cabecera =  fila_cabecera

    def cargar_fichero(self, flag_bbva = False):
        df = pl.read_excel(self.fichero)

        # 1. Tomar fila 6 (índice 5) como cabecera
        header = df.row(self.fila_cabecera)

        # 2. Convertir a strings, reemplazando None por un nombre genérico
        new_columns = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(header)]

        if flag_bbva:
            new_columns[7] = "Divisa2"

        # 3. Cortar datos desde la fila slice en adelante
        df = df.slice(self.fila_cabecera+1)

        # 4. Renombrar columnas
        df = df.rename({old: new.lower() for old, new in zip(df.columns, new_columns)})

        return df

