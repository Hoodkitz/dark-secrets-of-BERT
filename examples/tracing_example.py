"""Small example demonstrating how to initialize tracing for this repo."""
import os

from pytorch_pretrained_bert.tracing import init_tracing, trace_span, start_span


def main():
    # Try to use AI Toolkit's OTLP endpoint as default if available
    otlp = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
    tracer = init_tracing(service_name="dark-secrets-of-BERT", otlp_endpoint=otlp, console=True)

    @trace_span("example.work")
    def work(x):
        return x * 2

    with start_span("example.main"):
        print("Tracing enabled:", tracer is not None)
        print("work(3)", work(3))


if __name__ == "__main__":
    main()
