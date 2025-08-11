from typing import List
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.entities.user import UserEntity, UserEntityFactory
from app.application.services.user_service import UserService
from app.infrastructure.schemas.user_schema import (
    UserCreate,
    UserOutput,
    UserUpdate,
)
from app.infrastructure.container import Container

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserOutput])
@inject
async def get_all_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> List[dict]:
    try:
        users: List[UserEntity] = await user_service.get_all_users()
        return [user.__dict__ for user in users]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/email/{user_email}", response_model=UserOutput)
@inject
async def get_user_by_email(
    user_email: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    try:
        user = await user_service.get_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/id/{user_id}", response_model=UserOutput)
@inject
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado TESTE")
        return user.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_data: UserCreate,
    user_factory: UserEntityFactory = Depends(Provide[Container.user_factory]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    try:
        existing_user = await user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

        user_entity = user_factory.create(
            id=None,
            nome=user_data.nome,
            email=user_data.email,
            hashed_password=user_data.password,
            funcao=user_data.funcao,
        )
        created_user = await user_service.create_user(user_entity, user_data.password)
        return created_user.__dict__
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/id/{user_id}", response_model=UserOutput)
@inject
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_factory: UserEntityFactory = Depends(Provide[Container.user_factory]),
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> dict:
    try:
        existing_user = await user_service.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        updated_data = existing_user.__dict__.copy()
        if user_data.nome is not None:
            updated_data["nome"] = user_data.nome
        if user_data.email is not None:
            updated_data["email"] = user_data.email
        if user_data.funcao is not None:
            updated_data["funcao"] = user_data.funcao
        if user_data.password is not None:
            hashed = user_service.password_service.hash_password(user_data.password)
            updated_data["hashed_password"] = hashed

        user_entity = user_factory.create(**updated_data)
        updated_user = await user_service.update_user(user_entity)
        return updated_user.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/id/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    try:
        success = await user_service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
