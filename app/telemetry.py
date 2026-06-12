"""OpenTelemetry setup for GCP tracing, metrics and logging."""

import logging
import structlog
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

logger = structlog.get_logger(__name__)


def setup_telemetry(service_name: str = "agentic-ai-engine") -> None:
    """Configure OpenTelemetry with GCP Cloud Trace exporter.

    Sets up:
    - TracerProvider with GCP Cloud Trace export
    - Resource attributes for service identification
    """
    try:
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        from opentelemetry.resourcedetector.gcp_resource_detector import GoogleCloudResourceDetector

        # Detect GCP resource attributes (project, region, etc.)
        resource = Resource.create({SERVICE_NAME: service_name})

        # Set up Cloud Trace exporter
        exporter = CloudTraceSpanExporter()
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        logger.info("OpenTelemetry configured with Cloud Trace exporter", service=service_name)

    except ImportError:
        logger.warning("Cloud Trace exporter not available, using no-op tracer")
    except Exception as e:
        logger.warning("Failed to setup OpenTelemetry", error=str(e))