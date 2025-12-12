<!-- .github/copilot-instructions.md - concise guidance for AI coding agents -->

# Copilot / AI agent instructions for this repository

Purpose: Quickly onboard an AI coding agent to be productive in this small, self-contained BERT/Transformer tooling fork.

1) Big picture
- Core package: `pytorch_pretrained_bert/` — model definitions, tokenizers, weight-loading/conversion helpers, and optimization utilities.
- Examples: `examples/` contains runnable CLIs (e.g. `run_classifier.py`, `extract_features.py`, `run_gpt2.py`, `lm_finetuning/`). Use these to understand expected I/O and CLI flags.
- Tests: `tests/` mirror implementation files (unit-tests for modeling/tokenization/optimization). They are small and fast — a good source of intended behavior.

2) Key files to read first
- `pytorch_pretrained_bert/modeling.py` — central model wiring and public API used by examples/tests.
- `pytorch_pretrained_bert/tokenization.py` (+ `tokenization_gpt2.py`, `tokenization_openai.py`, `tokenization_transfo_xl.py`) — tokenizer contracts and normalization/token-piece behavior.
- `pytorch_pretrained_bert/convert_*_checkpoint_to_pytorch.py` — how TF/GPT/OpenAI checkpoints are converted and what state dict keys are expected.
- `optimization.py` / `optimization_openai.py` — learning rate schedules and optimizer helper utilities used in examples/lm_finetuning.

3) Developer workflows & useful commands
- Install for development: `pip install -e .` (project root contains `setup.py`).
- Install runtime deps: `pip install -r requirements.txt` (use an isolated virtualenv/conda).
- Run tests: `pytest -q tests` — tests are designed to validate tokenizer/model behavior.
- Run an example CLI to inspect args and expected behavior: `python examples/run_classifier.py --help` or `python examples/extract_features.py --help`.
- Build distributions (when releasing): `python setup.py sdist bdist_wheel` and upload with `twine`.

4) Project-specific conventions & patterns
- Package namespace: New models/helpers should live in `pytorch_pretrained_bert.*` so imports stay stable.
- Tokenizers: each model family uses a single tokenizer file. Preserve public methods (tokenize, convert_tokens_to_ids, convert_ids_to_tokens). Tests call these directly (see `tests/tokenization*_test.py`).
- Conversion scripts: keep heavy I/O and TensorFlow-specific logic inside `convert_*` scripts; examples expect PyTorch checkpoints/state dicts.
- Tests: follow existing pattern — name tests `*_test.py`, use fixtures in `tests/conftest.py`, and mirror behavior from implementation files.

5) Integration points & external dependencies
- Primary runtime dependency: `torch` (see `setup.py` for nominal minimum). Also depends on `numpy`, `requests`, `boto3`, `tqdm`, `regex`.
- External integrations: TensorFlow checkpoints and OpenAI/GPT2 formats via `convert_*` scripts. Check conversion scripts for assumptions about variable naming.
- Docker: `docker/Dockerfile` provides a reproducible runtime image useful for heavy I/O operations and conversion testing.

6) How to make safe changes (concrete examples)
- Adding a new model: create `pytorch_pretrained_bert/modeling_<name>.py`, export the class from `pytorch_pretrained_bert/modeling.py` or `__init__.py` if you want it to be discoverable by examples, and add a small unit test under `tests/` mirroring `modeling_test.py`.
- Changing tokenizer behavior: update the relevant `tokenization*.py` file and run `pytest tests/tokenization*_test.py` to validate normalization/tokenization edge cases.
- Updating conversion behavior: exercise `convert_*_checkpoint_to_pytorch.py` with a small saved TF/GPT checkpoint or add unit tests for the mapping logic. Keep heavy downloads out of CI.

7) Quick heuristics
- Preserve public API in `pytorch_pretrained_bert/*` unless explicitly bumping the package version.
- Prefer small, focused commits that update implementation + tests together.

Files of interest (examples):
- `pytorch_pretrained_bert/modeling.py` — model APIs and entry points used by `examples/` and `tests/`.
- `pytorch_pretrained_bert/tokenization.py` — the canonical tokenizer used by many examples.
- `examples/run_classifier.py`, `examples/extract_features.py`, `lm_finetuning/simple_lm_finetuning.py` — example usages and CLI patterns.

If something here is unclear or you want file-level edits (add a model, change a tokenizer, add tests), tell me which task and I will update the repository with a focused patch.
