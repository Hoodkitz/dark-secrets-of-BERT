"""Simple OpenTelemetry tracing helper for this repository.

This module provides an init_tracing function that configures OpenTelemetry
exporters and returns a tracer. All imports are guarded so the package
remains optional for users who don't install the tracing dependencies.
"""
from __future__ import annotations

import os
import contextlib
from functools import wraps
from typing import Optional

try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    OTEL_AVAILABLE = True
except Exception:
    trace = None  # type: ignore
    OTEL_AVAILABLE = False


def init_tracing(service_name: str = "pytorch_pretrained_bert", otlp_endpoint: Optional[str] = None, console: bool = True):
    """Initialize tracing.

    - If OpenTelemetry packages are not installed this is a no-op.
    - If `otlp_endpoint` is provided it configures the OTLP HTTP exporter.
    - If `console` is True, a ConsoleSpanExporter is added (useful for local testing).
    Returns an opentelemetry Tracer or None.
    """
    if not OTEL_AVAILABLE:
        return None

    # Configure resource (service name)
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    # Configure exporters/processors
    if otlp_endpoint is None:
        otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    if otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    if console:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    return tracer


def trace_span(name: Optional[str] = None):
    """Decorator/contextmanager to create a span for a function.

    Usage:
        @trace_span("my.operation")
        def fn(...):
            ...
    If OpenTelemetry is not installed, the decorator is a no-op.
    """
    def decorator(func):
        if not OTEL_AVAILABLE:
            return func

        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(func.__module__)
            span_name = name or f"{func.__module__}.{func.__name__}"
            with tracer.start_as_current_span(span_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


@contextlib.contextmanager
def start_span(name: str):
    """Context manager to start a span; no-op if OTEL not available."""
    if not OTEL_AVAILABLE:
        yield None
    else:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(name) as span:
            yield span
