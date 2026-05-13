# Repository Guidelines

## Project Structure & Module Organization
Core code lives under `src/casper_bot/`:
- `bot/` contains Telegram-facing code (`handlers/`, `middlewares/`, `router.py`, `keyboards/`).
- `agent/` contains reasoning/orchestration (`core.py`, `planner.py`, `executor.py`, `memory.py`).
- `tools/` implements concrete actions (for example `search.py`, `calendar.py`).
- `services/` wraps external integrations, `db/` handles models/repository/session, and `utils/` holds shared helpers.

Operational scripts are in `scripts/` (`run_bot.py`, `seed_db.py`, `index_workflows.py`). Tests are in `tests/` and should mirror source modules.

## Build, Test, and Development Commands
- `pip install -e .` installs the package in editable mode.
- `python -m casper_bot.main` runs the bot polling loop locally.
- `pytest tests/` runs the test suite.
- `python scripts/seed_db.py` seeds local database data for development.

If you use `uv`, equivalent commands are `uv pip install -e .` and `uv run pytest tests/`.

## Coding Style & Naming Conventions
Use Python 3.10+ with PEP 8 defaults:
- 4-space indentation, `snake_case` for functions/modules, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Keep handlers thin: route input and delegate logic to `agent/` or `tools/`.
- Keep prompts centralized in `agent/prompts.py`; keep DB access in `db/repository.py`.
- Prefer type hints on public functions and dataclass/model boundaries.

## Testing Guidelines
Use `pytest`. Name files as `tests/test_<module>.py` and test functions as `test_<behavior>()`.
Mirror source layout when adding tests (for example, changes in `agent/planner.py` should include `tests/test_planner.py`).
Cover happy-path and failure-path behavior for tools, handler routing, and agent decision flow.

## Commit & Pull Request Guidelines
This repository currently has no commit history baseline; use Conventional Commit style going forward:
- `feat: add calendar tool validation`
- `fix: handle missing TELEGRAM_BOT_TOKEN`

PRs should include:
- clear summary of user-facing or architectural change,
- linked issue/task (if available),
- test evidence (`pytest` output or explanation if tests are pending),
- notes on config/env changes (for example new `.env` keys).

## Security & Configuration Tips
Never commit secrets. Keep tokens/URLs in `.env`, and update `.env.example` when adding required settings.
