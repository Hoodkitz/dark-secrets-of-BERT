# Contributing

Thanks for contributing! This file describes the minimal workflow and conventions used in this repository.

Development setup
- Create and activate a virtualenv / conda env.
- Install editable package and dev deps:

```bash
pip install -e .
pip install -r requirements.txt
pip install -r requirements.txt  # tests use pytest
```

Run the tests
- Fast: `pytest -q tests`

Project layout & conventions
- Core package: `pytorch_pretrained_bert/` — add new models/helpers under this namespace.
- Tokenizers: per-model tokenizer files (e.g. `tokenization.py`, `tokenization_gpt2.py`). Keep public API: `tokenize`, `convert_tokens_to_ids`, `convert_ids_to_tokens`.
- Conversion scripts: `convert_*_checkpoint_to_pytorch.py` are CLIs that assume TF/OpenAI variable naming — keep heavy I/O isolated.
- Tests: add `*_test.py` under `tests/` and mirror style from existing tests. Use fixtures in `tests/conftest.py`.

Making changes
- Small, focused commits are preferred. One logical change per PR.
- Update or add unit tests for behavior changes. Run `pytest -q tests` locally.
- Preserve public API in `pytorch_pretrained_bert/*` unless you document a version bump in the PR.

Adding a new model example
1. Create `pytorch_pretrained_bert/modeling_<name>.py` and implement model.
2. Export the model (import) from `pytorch_pretrained_bert/modeling.py` or `__init__.py` for discoverability in examples.
3. Add a small unit test under `tests/` that mirrors `modeling_test.py`.

Changing tokenization
- Update the corresponding `tokenization*.py` file.
- Add or update `tests/tokenization*_test.py` and run `pytest -q tests/tokenization*_test.py`.

Conversion scripts
- These scripts convert TF/OpenAI checkpoints to PyTorch; run them locally with small checkpoints for testing.
- Avoid heavy network downloads in CI.

Release & packaging
- Build distributions: `python setup.py sdist bdist_wheel`.

Contact
- If uncertain about a change, open an issue describing intent and link to a small PR draft.
