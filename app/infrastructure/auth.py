import os
from datetime import datetime, timedelta
from typing import Optional

import newrelic.agent
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.infrastructure.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está definida no .env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica o token JWT e retorna o payload.
    
    O payload pode conter:
    - sub: ID do usuário
    - trace_id: ID do trace para correlação (vindo do Lambda)
    - exp: Data de expiração
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        trace_id = payload.get("trace_id") or payload.get("traceId")
        if trace_id:
            _propagate_trace_to_newrelic(trace_id, payload)
        
        return payload
    except JWTError as e:
        logger.warning(
            "Failed to decode JWT token",
            extra={"error": str(e), "error_type": type(e).__name__}
        )
        return None


def _propagate_trace_to_newrelic(trace_id: str, payload: dict) -> None:
    """Propaga o trace_id do JWT para o New Relic."""
    try:
        newrelic.agent.add_custom_attribute("lambda_trace_id", trace_id)
        newrelic.agent.add_custom_attribute("jwt_user_id", payload.get("sub", ""))
        
        if isinstance(trace_id, str) and len(trace_id) > 10:
            newrelic.agent.accept_distributed_trace_payload(trace_id, transport_type="HTTP")
            logger.debug("Accepted distributed trace from Lambda", extra={"trace_id": trace_id[:16] + "..."})
    except Exception as e:
        logger.debug("Failed to propagate trace to New Relic", extra={"error": str(e)})
