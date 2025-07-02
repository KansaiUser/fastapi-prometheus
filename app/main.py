from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from middleware import MetricsMiddleware

app = FastAPI()

app.add_middleware(MetricsMiddleware)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI with Prometheus"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
