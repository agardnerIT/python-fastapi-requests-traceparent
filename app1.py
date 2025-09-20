from fastapi import FastAPI
import uvicorn
import requests

# Usage
# pip install -r requirements.txt
# python app1.py

# OpenTelemetry imports
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider
from opentelemetry import trace
#from opentelemetry.instrumentation.requests import RequestsInstrumentor

PORT = 8080
APP_NAME = "app1"

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
#RequestsInstrumentor().instrument()

@app.get("/")
async def read_root():

    print(f"I am {APP_NAME} running on {PORT}. Here are my trace details: {trace.get_current_span()}")

    response = requests.get("http://localhost:8090/")
    print(f"I am {APP_NAME} running on {PORT}. Here is what I'm sending out: {response.request.headers}, {response.request.method}, {response.request.url}")
    
    return {"microservice2_response_code": response.status_code, "microservice2_response": response.json()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
