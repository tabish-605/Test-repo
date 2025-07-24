from opentelemetry import trace, propagate
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.propagators.aws.xray import AWSXRayPropagator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


def setup_tracing(app, engine):
    resource = Resource.create({"service.name": "backend-api"})
    provider = TracerProvider(resource=resource, id_generator=AwsXRayIdGenerator())
    otlp_exporter = OTLPSpanExporter(endpoint="http://collector:4317", insecure=True)
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)
    propagate.set_global_textmap(AWSXRayPropagator())
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    SQLAlchemyInstrumentor().instrument(engine=engine)
