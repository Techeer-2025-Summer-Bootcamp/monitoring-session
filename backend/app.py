from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("fastapi")

# Set up OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize FastAPI app
app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

app = FastAPI()


@app.get("/")
async def root():
    with tracer.start_as_current_span("root") as span:
        span.set_attribute("test", "test")
        span.add_event("test_event", {"test": "test"})
        span.set_status(trace.Status(trace.StatusCode.ERROR, "test error"))
        time.sleep(2)
        span.end()
    return {"message": "Hello World"}