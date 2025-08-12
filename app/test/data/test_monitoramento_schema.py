import pytest
from pydantic import ValidationError
from app.infrastructure.schemas.monitoramento_schema import TempoMedioServicosOut

class TestTempoMedioServicosOut:

    def test_valid_tempo_medio(self):
        tempo = TempoMedioServicosOut(dias=1, horas=2, minutos=30)
        assert tempo.dias == 1
        assert tempo.horas == 2
        assert tempo.minutos == 30