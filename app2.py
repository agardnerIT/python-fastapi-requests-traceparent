from fastapi import FastAPI, Request
import uvicorn

# Usage
# pip install -r requirements.txt
# python app2.py

# OpenTelemetry imports
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider
from opentelemetry import trace

PORT=8090
APP_NAME = "app2"

app = FastAPI()

# Set up OpenTelemetry tracing with OTLP HTTP exporter
resource = Resource(attributes={
    SERVICE_NAME: APP_NAME
})
tracer_provider = TracerProvider(resource=resource)
set_tracer_provider(tracer_provider)

# Configure OTLP HTTP exporter (default endpoint: http://localhost:4318/v1/traces)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces"  # Adjust if your collector is at a different address
)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def read_root(request: Request):

    print(f"I am {APP_NAME}. Here is what I received: {request.headers}, {request.method}, {request.url}")

    print(f"I am {APP_NAME} running on {PORT}. Here are my trace details: {trace.get_current_span()}")
    return {"service_status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
