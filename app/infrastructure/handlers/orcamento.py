from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from app.infrastructure.container import Container
from app.application.services.orcamento import OrcamentoService
from app.infrastructure.schemas.orcamento import OrcamentoOutput

router = APIRouter(prefix="/ordens-servico", tags=["orcamento"])


@router.get(
    "/{ordem_servico_id}/orcamento", 
    response_model=OrcamentoOutput
)
@inject
async def gerar_orcamento(
    ordem_servico_id: str,
    service: OrcamentoService = Depends(Provide[Container.orcamento_service]),
):
    try:
        orcamento = await service.gerar_orcamento(ordem_servico_id)
        return orcamento.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
