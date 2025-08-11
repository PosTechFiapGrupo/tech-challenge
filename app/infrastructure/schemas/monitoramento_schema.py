from pydantic import BaseModel
from typing import Optional

class TempoMedioServicosOut(BaseModel):
    dias: int
    horas: int
    minutos: int