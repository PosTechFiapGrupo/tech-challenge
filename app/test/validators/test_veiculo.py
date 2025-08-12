import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from app.application.validators.veiculo import VeiculoValidator

@pytest.mark.asyncio
async def test_validate_exists_success():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = {"id": 123, "model": "Carro XYZ"}  # simula veículo existente
    
    validator = VeiculoValidator(vehicle_repository=mock_repo)
    
    # Deve completar sem erro
    await validator.validate_exists(123)
    
    mock_repo.get_by_id.assert_awaited_once_with(123)

@pytest.mark.asyncio
async def test_validate_exists_not_found():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None  # simula veículo não encontrado
    
    validator = VeiculoValidator(vehicle_repository=mock_repo)
    
    with pytest.raises(HTTPException) as exc_info:
        await validator.validate_exists(999)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Veículo não encontrado"
    mock_repo.get_by_id.assert_awaited_once_with(999)
