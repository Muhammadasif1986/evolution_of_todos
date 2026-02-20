from fastapi import Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging

logger = logging.getLogger(__name__)

# Initialize tracer provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

def setup_tracing(app):
    """Set up distributed tracing for the application."""

    # Set up OTLP exporter for tracing
    try:
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://jaeger:4317",  # Jaeger endpoint
            insecure=True,
        )

        # Add span processor
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        logger.info("Tracing configured with OTLP exporter")
    except Exception as e:
        logger.warning(f"Could not configure OTLP tracing: {e}")
        # Set up a console exporter as fallback
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
        span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        trace.get_tracer_provider().add_span_processor(span_processor)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy
    # This will be handled when database engine is created
    # SQLAlchemyInstrumentor().instrument()

    # Instrument requests (for outbound HTTP calls)
    RequestsInstrumentor().instrument()

    logger.info("Distributed tracing setup completed")


def get_tracer():
    """Get the tracer instance."""
    return tracer