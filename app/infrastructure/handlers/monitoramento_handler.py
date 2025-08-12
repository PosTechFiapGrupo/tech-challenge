from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.repositories.ordem_servico_impl import OrdemServicoRepositoryImpl
from app.application.services.monitoramento_service import MonitoramentoService
from app.infrastructure.schemas.monitoramento_schema import TempoMedioServicosOut
from app.infrastructure.auth_dependencies import role_required
from datetime import timedelta

router = APIRouter(prefix="/monitoramento", tags=["Monitoramento"])

def format_timedelta(td: timedelta) -> str:
    total_segundos = int(td.total_seconds())
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{dias} dias, {horas} horas, {minutos} minutos"

@router.get("/tempo-medio-servicos", response_model=TempoMedioServicosOut, dependencies=[Depends(role_required("admin", "atendente"))])
async def tempo_medio_servicos():
    repo = OrdemServicoRepositoryImpl()
    service = MonitoramentoService(repo)
    tempo_medio = await service.obter_tempo_medio()
    if tempo_medio is None:
        raise HTTPException(status_code=404, detail="Nenhum serviço finalizado")

    total_segundos = int(tempo_medio.total_seconds())
    dias, resto = divmod(total_segundos, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)

    return TempoMedioServicosOut(
        dias=dias,
        horas=horas,
        minutos=minutos,
    )