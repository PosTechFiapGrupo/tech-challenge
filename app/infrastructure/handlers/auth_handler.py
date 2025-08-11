from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.application.services.user_service import UserService
from app.infrastructure.auth import create_access_token, verify_password
from app.infrastructure.container import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
@inject
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    user = await user_service.get_user_by_email(username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id), "role": user.funcao})
    return {"access_token": access_token, "token_type": "bearer"}
