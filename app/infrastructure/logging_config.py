import json
import logging
import os
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Optional

import newrelic.agent

# Context variables para correlação de requisições
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


def get_newrelic_linking_metadata() -> dict:
    """Obtém metadados de linking do New Relic para correlação de traces."""
    try:
        return newrelic.agent.get_linking_metadata() or {}
    except Exception:
        return {}


class JSONFormatter(logging.Formatter):
    """
    Formatter que produz logs estruturados em JSON.
    
    Inclui automaticamente:
    - Timestamp ISO 8601
    - Nível de log
    - Nome do logger
    - Mensagem
    - trace_id, span_id do New Relic
    - request_id da requisição atual
    - Metadados Kubernetes
    """
    
    def format(self, record: logging.LogRecord) -> str:
        # Obter metadados do New Relic
        nr_metadata = get_newrelic_linking_metadata()
        
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Adicionar trace context do New Relic
        if nr_metadata:
            log_entry["trace.id"] = nr_metadata.get("trace.id", "")
            log_entry["span.id"] = nr_metadata.get("span.id", "")
            log_entry["entity.name"] = nr_metadata.get("entity.name", "")
            log_entry["entity.type"] = nr_metadata.get("entity.type", "")
            log_entry["hostname"] = nr_metadata.get("hostname", "")
        
        # Adicionar request_id e trace_id da context var (do JWT/Lambda)
        request_id = request_id_var.get()
        if request_id:
            log_entry["request_id"] = request_id
        
        trace_id_from_jwt = trace_id_var.get()
        if trace_id_from_jwt:
            log_entry["external_trace_id"] = trace_id_from_jwt
        
        user_id = user_id_var.get()
        if user_id:
            log_entry["user_id"] = user_id
        
        # Adicionar metadados Kubernetes (via env vars)
        k8s_metadata = {
            "kubernetes.cluster_name": os.getenv("NEW_RELIC_METADATA_KUBERNETES_CLUSTER_NAME"),
            "kubernetes.namespace": os.getenv("NEW_RELIC_METADATA_KUBERNETES_NAMESPACE_NAME"),
            "kubernetes.pod_name": os.getenv("NEW_RELIC_METADATA_KUBERNETES_POD_NAME"),
            "kubernetes.node_name": os.getenv("NEW_RELIC_METADATA_KUBERNETES_NODE_NAME"),
            "kubernetes.container_name": os.getenv("NEW_RELIC_METADATA_KUBERNETES_CONTAINER_NAME"),
        }
        log_entry["kubernetes"] = {k: v for k, v in k8s_metadata.items() if v}
        
        # Adicionar exception info se existir
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Adicionar campos extras do record
        if hasattr(record, 'extra_fields'):
            log_entry["extra"] = record.extra_fields
        
        return json.dumps(log_entry, ensure_ascii=False, default=str)


class ContextualLogger(logging.LoggerAdapter):
    """
    Logger adapter que adiciona contexto automaticamente aos logs.
    """
    
    def process(self, msg: str, kwargs: dict) -> tuple[str, dict]:
        extra = kwargs.get('extra', {})
        
        # Adicionar contexto das context vars
        if request_id := request_id_var.get():
            extra['request_id'] = request_id
        if trace_id := trace_id_var.get():
            extra['external_trace_id'] = trace_id
        if user_id := user_id_var.get():
            extra['user_id'] = user_id
        
        kwargs['extra'] = extra
        return msg, kwargs


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configura o logging estruturado para toda a aplicação.
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Obter nível de log do ambiente ou usar o padrão
    level = os.getenv("LOG_LEVEL", log_level).upper()
    
    # Criar handler com formato JSON para stdout
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(JSONFormatter())
    
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level, logging.INFO))
    
    # Remover handlers existentes e adicionar o JSON handler
    root_logger.handlers.clear()
    root_logger.addHandler(json_handler)
    
    # Configurar loggers específicos
    for logger_name in ["app", "uvicorn", "uvicorn.access", "uvicorn.error", "gunicorn", "gunicorn.access", "gunicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, level, logging.INFO))
        logger.handlers.clear()
        logger.addHandler(json_handler)
        logger.propagate = False
    
    # Reduzir verbosidade de loggers muito detalhados
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


def get_logger(name: str) -> ContextualLogger:
    """
    Obtém um logger contextual para o módulo especificado.
    
    Args:
        name: Nome do logger (geralmente __name__)
    
    Returns:
        ContextualLogger com contexto automático
    """
    return ContextualLogger(logging.getLogger(name), {})
