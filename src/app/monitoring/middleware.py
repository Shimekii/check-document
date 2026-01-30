import time
from fastapi import Request

from app.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY

async def prometheus_middleware(request: Request, call_next):

    # ⛔ исключаем metrics ЖЁСТКО
    if request.scope["path"].startswith("/metrics"):
        return await call_next(request)

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    route = request.scope.get("route")
    path = route.path if route else request.url.path

    REQUEST_COUNT.labels(
        method=request.method,
        path=path,
        status=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=path,
        status=str(response.status_code),
    ).observe(process_time)

    return response