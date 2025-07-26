from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
from starlette.requests import Request
import time

# REQUEST_COUNT = Counter(
#     "http_requests_total",
#     "Total number of HTTP requests",
#     ["app_name", "method", "endpoint", "http_status"]
# )
REQUEST_COUNT = Counter(
    name='http_request_count',
    documentation='Total number of HTTP requests',
    labelnames=['app_name', 'method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    name='http_request_latency_seconds',
    documentation='Request latency',
    labelnames=['app_name', 'endpoint']
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        REQUEST_LATENCY.labels(
            app_name="webapp",
            endpoint=request.url.path
        ).observe(process_time)

        REQUEST_COUNT.labels(
            app_name="webapp",
            method=request.method,
            endpoint=request.url.path,
            http_status=str(response.status_code)
        ).inc()

        return response