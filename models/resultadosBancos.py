from dataclasses import Field
from datetime import datetime

from pydantic import BaseModel, ConfigDict



class resultadoBancos(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True, populate_by_name=True)

    fecha: datetime = Field(alias= "fecha")
    concep: str = Field(alias= "concepto")
    imp: float = Field(alias= "importe")
    saldo: float = Field(alias= "saldo_total")
    
