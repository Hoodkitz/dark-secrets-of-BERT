<!-- .github/copilot-instructions.md - concise guidance for AI coding agents -->

# Copilot / AI agent instructions for this repository

Purpose: quickly orient an AI coding agent to be productive in this repo (a small, self-contained fork of early Transformer/BERT tooling).

1) Big picture
- This repo centers on the `pytorch_pretrained_bert` package: model definitions, tokenizers, and optimization utilities live under `pytorch_pretrained_bert/`.
- Examples and runnable scripts are under `examples/` (e.g. `run_classifier.py`, `extract_features.py`, `lm_finetuning/`). Tests live in `tests/` and mirror implementation files (e.g. `tokenization_test.py`).
- Conversion scripts (`convert_*_checkpoint_to_pytorch.py`) provide integration points with TF / GPT2 / OpenAI checkpoints.

2) Key files and entry points (read first)
- `pytorch_pretrained_bert/modeling.py` — central model class wiring and public API.
- `pytorch_pretrained_bert/tokenization.py` and `tokenization_*.py` — tokenization contracts used across examples and tests.
- `optimization.py` / `optimization_openai.py` — optimizer-related helpers and learning-rate schedules.
- `examples/*` — scripts that show how CLI args drive data/model I/O.
- `tests/` — small pytest-based unit tests; follow their patterns when adding tests.

3) Developer workflows (commands an agent may need to suggest/run)
- Install for development: `pip install -e .` (root contains `setup.py`).
- Install deps: `pip install -r requirements.txt` (use virtualenv/conda).
- Run unit tests: `pytest -q tests` (tests are small and fast).
- Build distribution: `python setup.py sdist bdist_wheel`.
- Run example scripts: `python examples/run_classifier.py --help` or run the specific example script you modify.

4) Project-specific conventions & patterns
- Namespaces: package code lives in `pytorch_pretrained_bert.*` — prefer adding new modules in this package to keep API coherence.
- Tokenizers are single-file implementations (e.g. `tokenization.py`, `tokenization_gpt2.py`) — keep tokenizer public methods compatible with existing calls in `examples/`.
- Conversion scripts are one-off CLIs that produce PyTorch checkpoint files; keep unfamiliar heavy I/O isolated to `convert_*_` scripts.
- Tests follow `*_test.py` naming and use plain pytest fixtures in `tests/conftest.py`.

5) Integration points & external dependencies
- Check `requirements.txt` for runtime/test deps. Major integrations: TensorFlow checkpoints (via conversion scripts), GPT-2/OpenAI conversion utilities.
- Docker image: `docker/Dockerfile` shows a self-contained runtime—useful when reproducing environment issues.

6) How to make safe changes (practical examples)
- Adding a new model: add `pytorch_pretrained_bert/modeling_<name>.py`, expose an import in `__init__.py` or `modeling.py`, and add a small unit test under `tests/` mirroring existing tests.
- Tokenizer change: update corresponding `tokenization*.py` and run `tests/tokenization*_test.py`.

7) Quick heuristics for patches
- Preserve public API in `pytorch_pretrained_bert/*` unless bumping major version.
- Run `pytest -q tests` after edits; ensure conversion scripts still run (they are I/O heavy — run locally if needed).

If anything above is unclear or you want examples tailored to a specific change (add model, change tokenizer, update an example), tell me which task and I'll expand with file-level guidance and a small patch.
