import polars as pl
import sys
from utils.parseos import parse_datetime_expr as make_dt
from utils.filtrados import Filtros
from etl import Etl

sys.stdout.reconfigure(encoding="utf-8")

pl.Config.set_tbl_rows(100)

dataIng = "../data/raw/Santander/santander_010825_310825.xls"

df = pl.read_excel(dataIng)

# 1. Tomar fila 6 (índice 5) como cabecera
header = df.row(4)
print(header)

# 2. Convertir a strings, reemplazando None por un nombre genérico
new_columns = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(header)]

# 3. Cortar datos desde la fila 7 en adelante
df = df.slice(5)

print(df)
# 4. Renombrar columnas
df = df.rename({old: new.lower() for old, new in zip(df.columns, new_columns)})

#df = Etl("../data/raw/BBVA/bbva_010825_310825.xlsx").cargar_fichero()

# 5. Castaer las columnas y renombrar columnas
print("columnas son:", df.columns)
dict_columns = {"f. valor": "fecha_valor",
        "subcategoría": "movimiento",
        "descripción": "concepto",
        "importe (€)": "importe",
        "saldo (€)": "saldo",}
df = (
    df
    .rename(dict_columns)
)

fv = pl.col("fecha_valor")

# Intenta varios formatos y quédate con el primero válido
parsed_dt = make_dt(fv)

df = (df
    .with_columns([
        parsed_dt.dt.date().alias("fecha_valor"),  # convertir a Date
        pl.col("importe").cast(pl.Float64),
        pl.col("saldo").cast(pl.Float64),
    ])
    .drop(["comentario", "imagen"]))

df_filtro = Filtros(df)

df_filtro = df_filtro.modificar_conceptos()

df_filtro.write_csv("prueba")

