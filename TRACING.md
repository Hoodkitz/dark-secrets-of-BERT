Tracing (OpenTelemetry)
========================

This repository includes an optional lightweight OpenTelemetry tracing helper.

Files added
- `pytorch_pretrained_bert/tracing.py` — guarded OpenTelemetry initialization helper and small utilities (`init_tracing`, `trace_span`, `start_span`).
- `examples/tracing_example.py` — minimal example showing usage.

How to enable

1. Install the optional tracing dependencies (locally or in your environment):

```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation
```

2. Run the example or import `pytorch_pretrained_bert.tracing` and call `init_tracing()` early in your process.

AI Toolkit (optional): If you use the AI Toolkit trace viewer, open the trace collector (VS Code command `ai-mlstudio.tracing.open`) and use the OTLP endpoint `http://localhost:4318` (HTTP) or `http://localhost:4317` (gRPC).

Notes
- The tracing helper is guarded: if OpenTelemetry packages are not installed, importing the module is safe and functions are no-ops.
- The example enables a console exporter by default for easy local debugging.
