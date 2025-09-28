from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator



class BaseModelBancos(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_to_lower=True, populate_by_name=True)

    fecha_val: datetime = Field(alias="fecha_valor")
    concep: str = Field(alias="concepto")
    imp: float = Field(alias="importe")
    saldo: float = Field(alias="saldo")


    # Parseo DD/MM/YYYY -> datetime
    @field_validator("fecha_op", "fecha_val", mode="before", check_fields=False)
    @classmethod
    def parse_ddmmyyyy(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%d/%m/%Y")
        return v

    @field_validator("cuenta", mode="before", check_fields=False)
    @classmethod
    def normalize_iban(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "").upper()  # quita espacios y pasa a MAYÚSCULAS
        return v

class ModelSantander(BaseModelBancos):

    fecha_op: datetime = Field(alias="fecha_operacion")
    cuenta: str = Field(alias = "cuenta", pattern=r"[A-Z]{2}[0-9]{22}", default="ES4600493490622114023051")


class ModelBbva(BaseModelBancos):

    fecha_op: datetime = Field(alias="fecha_operacion")
    mov: str = Field(alias="movimiento")
    divisa: str = Field(alias="divisa")
    obser: str = Field(alias="observaciones")

class ModelIng(BaseModelBancos):
    cat: str = Field(alias="categoria")
    subcat: str = Field("movimiento")


santan = ModelSantander(fecha_operacion="12/09/2025",fecha_valor="12/09/2025" ,
                        concepto="Transferencia De Sergio Suarez Checa, Concepto Movimiento Ing.",importe=900, saldo=2301.78)
bbva = ModelBbva(fecha_operacion="12/09/2025",fecha_valor="12/09/2025",
                        concepto="Transferencia De Sergio Suarez Checa, Concepto Movimiento Ing.",importe=900, saldo=2301.78,
                 movimiento="Pago con tarjeta", divisa="EUR", observaciones="4188202151703996 MCAFEE*AUTORENEWAL")

print(santan)
print(bbva)



