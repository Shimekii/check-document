from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/healthz",
    tags=["system"],
)

@router.get("/live")
async def liveness_probe() -> JSONResponse:
    """
    Простая проверка на то, что приложение запущено и работает.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={'status': 'ok'})
