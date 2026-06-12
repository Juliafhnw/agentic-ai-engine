"""OpenTelemetry setup for GCP tracing, metrics and logging."""

import os
import structlog

logger = structlog.get_logger(__name__)


def setup_telemetry(service_name: str = "agentic-ai-engine") -> None:
    """Configure OpenTelemetry with GCP Cloud Trace exporter."""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.resources import Resource, SERVICE_NAME
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

        resource = Resource.create({SERVICE_NAME: service_name})
        exporter = CloudTraceSpanExporter()
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        logger.info("OpenTelemetry configured with Cloud Trace exporter", service=service_name)

    except Exception as e:
        logger.warning("OpenTelemetry setup skipped", error=str(e))