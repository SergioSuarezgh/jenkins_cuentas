import polars as pl
import re
from constantes.conceptos import conceptos


class Filtros:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    def modificar_conceptos(self) -> pl.DataFrame:
        # Normalizamos: pasamos "concepto" a mayúsculas y sustituimos null por cadena vacía
        concepto_up = pl.col("concepto").cast(pl.Utf8).fill_null("").str.to_uppercase()


        df = self.df.with_columns(pl.lit(None, dtype=pl.Utf8).alias("Prueba"))

        print("Df en funciones: ", df)

        # Construimos la cascada: el primer patrón que haga match gana
        # Usamos literal=True y comparamos en mayúsculas para hacerlo case-insensitive
        for k, v in conceptos.items():
            patt = re.escape(k.upper())
            print("la key es: ",k.upper())
            print("el concept es: ", df.with_columns(
                  pl.col("concepto").cast(pl.Utf8).fill_null("").str.to_uppercase()).select("concepto"))
            print("hace match?: ",  df.with_columns(
                  pl.when(concepto_up.str.contains(k, literal=True)).then(pl.lit(v)).otherwise(pl.col("Prueba"))))
            df = (df
                  .with_columns(
                    pl.when(concepto_up.str.contains(k, literal=True)).then(pl.lit(v)).otherwise(pl.col("Prueba")).alias("Prueba")
                  )

            )

        return df.fill_null("Otros")



