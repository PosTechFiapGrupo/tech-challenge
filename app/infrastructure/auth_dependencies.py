from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import Provide, inject
from app.infrastructure.container import Container
from app.domain.entities.user import UserEntity
from app.infrastructure.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository = Depends(Provide[Container.user_repository]),
) -> UserEntity:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = await user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user

def role_required(*allowed_roles: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.funcao not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return current_user
    return role_checker
