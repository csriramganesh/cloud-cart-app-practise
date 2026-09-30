import time

from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter(
    "cloudcart_http_requests_total",
    "Total HTTP requests",
    [
        "method",
        "path",
        "status",
    ],
)


REQUEST_LATENCY = Histogram(
    "cloudcart_http_request_duration_seconds",
    "HTTP request duration",
    [
        "method",
        "path",
    ],
)


ERROR_COUNT = Counter(
    "cloudcart_http_errors_total",
    "Total HTTP errors",
    [
        "method",
        "path",
    ],
)


async def metrics_middleware(
    request,
    call_next,
):
    start = time.time()

    try:
        response = await call_next(request)

    except Exception:
        ERROR_COUNT.labels(
            method=request.method,
            path=request.url.path,
        ).inc()

        raise

    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        path=request.url.path,
    ).observe(duration)

    if response.status_code >= 500:
        ERROR_COUNT.labels(
            method=request.method,
            path=request.url.path,
        ).inc()

    return response
