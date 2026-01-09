import base64
import json
import time
import uuid
from typing import Callable, Optional

import newrelic.agent
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.infrastructure.logging_config import (
    get_logger,
    request_id_var,
    trace_id_var,
    user_id_var,
)

logger = get_logger(__name__)


def _decode_jwt_payload(request: Request) -> Optional[dict]:
    """Decodifica o payload do JWT sem verificação de assinatura."""
    try:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header[7:]
        parts = token.split(".")
        if len(parts) != 3:
            return None
        
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        
        return json.loads(base64.urlsafe_b64decode(payload_b64))
    except Exception:
        return None


def extract_trace_id_from_jwt(request: Request) -> Optional[str]:
    """Extrai o trace_id do JWT token no header Authorization."""
    payload = _decode_jwt_payload(request)
    if not payload:
        return None
    return payload.get("trace_id") or payload.get("traceId") or payload.get("x-trace-id")


def extract_user_id_from_jwt(request: Request) -> Optional[str]:
    """Extrai o user_id (sub) do JWT token."""
    payload = _decode_jwt_payload(request)
    return payload.get("sub") if payload else None


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Middleware para observabilidade completa das requisições.
    
    Funcionalidades:
    - Gera request_id único para cada requisição
    - Extrai e propaga trace_id do JWT para New Relic
    - Registra métricas de latência
    - Adiciona custom attributes no New Relic
    - Logs estruturados de entrada e saída
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Gerar request_id único
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Extrair trace_id do JWT (colocado pelo Lambda)
        trace_id = extract_trace_id_from_jwt(request)
        
        # Extrair user_id do JWT
        user_id = extract_user_id_from_jwt(request)
        
        # Configurar context vars para logging contextual
        request_id_token = request_id_var.set(request_id)
        trace_id_token = trace_id_var.set(trace_id) if trace_id else None
        user_id_token = user_id_var.set(user_id) if user_id else None
        
        # Adicionar custom attributes no New Relic
        self._add_newrelic_attributes(request_id, trace_id, user_id, request)
        
        # Iniciar timer para latência
        start_time = time.perf_counter()
        
        # Log de entrada
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("User-Agent"),
            }
        )
        
        try:
            response = await call_next(request)
            
            # Calcular latência
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Adicionar headers de correlação na resposta
            response.headers["X-Request-ID"] = request_id
            if trace_id:
                response.headers["X-Trace-ID"] = trace_id
            
            # Registrar métrica de latência no New Relic
            self._record_latency_metric(request, latency_ms, response.status_code)
            
            # Log de saída
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "latency_ms": round(latency_ms, 2),
                }
            )
            
            return response
            
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            
            # Log de erro
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "latency_ms": round(latency_ms, 2),
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                exc_info=True
            )
            
            # Registrar erro no New Relic
            self._notice_error(e)
            
            raise
            
        finally:
            # Limpar context vars
            request_id_var.reset(request_id_token)
            if trace_id_token:
                trace_id_var.reset(trace_id_token)
            if user_id_token:
                user_id_var.reset(user_id_token)
    
    def _add_newrelic_attributes(
        self,
        request_id: str,
        trace_id: Optional[str],
        user_id: Optional[str],
        request: Request
    ) -> None:
        """Adiciona custom attributes na transação do New Relic."""
        try:
            newrelic.agent.add_custom_attribute("request_id", request_id)
            newrelic.agent.add_custom_attribute("api_path", request.url.path)
            newrelic.agent.add_custom_attribute("http_method", request.method)
            
            if trace_id:
                newrelic.agent.add_custom_attribute("external_trace_id", trace_id)
                newrelic.agent.accept_distributed_trace_payload(trace_id, transport_type="HTTP")
            
            if user_id:
                newrelic.agent.add_custom_attribute("user_id", user_id)
        except Exception:
            pass
    
    def _record_latency_metric(self, request: Request, latency_ms: float, status_code: int) -> None:
        """Registra métrica customizada de latência no New Relic."""
        try:
            newrelic.agent.record_custom_metric(f"Custom/API/Latency/{request.method}{request.url.path}", latency_ms)
            newrelic.agent.record_custom_metric("Custom/API/Latency/All", latency_ms)
            newrelic.agent.record_custom_metric(f"Custom/API/StatusCode/{status_code // 100}xx", 1)
        except Exception:
            pass
    
    def _notice_error(self, error: Exception) -> None:
        """Registra erro no New Relic."""
        try:
            newrelic.agent.notice_error()
        except Exception:
            pass


class OrdemServicoMetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware específico para métricas de Ordens de Serviço.
    
    Registra eventos e métricas relacionadas ao processamento
    de ordens de serviço para alertas e dashboards.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Identificar se é uma rota de ordem de serviço
        path = request.url.path
        is_ordem_servico = path.startswith("/ordens-servico")
        
        response = await call_next(request)
        
        if is_ordem_servico:
            self._record_ordem_servico_event(request, response)
        
        return response
    
    def _record_ordem_servico_event(self, request: Request, response: Response) -> None:
        """Registra evento customizado para ordens de serviço."""
        try:
            event_data = {
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "success": response.status_code < 400,
            }
            
            if response.status_code >= 400:
                newrelic.agent.record_custom_event("OrdemServicoError", event_data)
                newrelic.agent.record_custom_metric("Custom/OrdemServico/Errors", 1)
            else:
                newrelic.agent.record_custom_event("OrdemServicoSuccess", event_data)
                
            newrelic.agent.record_custom_metric("Custom/OrdemServico/Operations", 1)
        except Exception:
            pass
