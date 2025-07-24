# backend/app/instrumentation.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def setup_tracing(app):
    # Set up OpenTelemetry resource information
    resource = Resource(attributes={
        "service.name": "ecommerce-api"
    })

    # Set up a tracer provider
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    # Set up an OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        # The endpoint for the OTel Collector, provided via environment variable
        # Defaults to a local collector instance.
        endpoint="http://otel-collector:4317",
        insecure=True
    )

    # Use a BatchSpanProcessor to send spans in batches
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # Instrument Psycopg2 for database tracing
    Psycopg2Instrumentor().instrument()
