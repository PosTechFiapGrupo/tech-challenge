from json import dumps
from fastapi import APIRouter, Response


router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> Response:
    return Response(status_code=200,
                    content=dumps({"status": "Healthy"}),
                    media_type="application/json")

@router.get("/ready")
async def readiness_check() -> Response:
    return Response(status_code=200,
                    content=dumps({"status": "Ready"}),
                    media_type="application/json")
