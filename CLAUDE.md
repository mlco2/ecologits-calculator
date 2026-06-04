# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync --group dev          # Install all dependencies including dev tools
uv run streamlit run app.py  # Start the app at http://localhost:8501
uv run pytest tests/ -v      # Run all tests
uv run pytest tests/test_formatting.py::test_name  # Run a single test
uv run ruff check --fix && uv run ruff format  # Lint and format
```

## Architecture

**EcoLogits Calculator** is a Streamlit app that estimates the environmental impact (energy, CO₂, water) of generative AI inference. It wraps the `ecologits` library for impact calculations and is deployed to Hugging Face Spaces.

**Entry point**: `app.py` — sets up the page and routes to one of four calculator modes.

**Four layers under `src/`**:

- `config/` — constants (prompt templates, usage intensities, model lists), UI text content, pydantic-style data models
- `core/` — pure functions: unit registry (`pint`), environmental equivalences, impact formatting
- `repositories/` — data access: loads AI model metadata from the `ecologits` library, electricity mix by country
- `ui/` — Streamlit components per mode: `calculator.py` (standard + expert), `company.py` + `expert_company.py` (organization-level footprint), `token_estimator.py`, plus shared `impacts.py`, `components.py`, `plotting.py`

**Data flow**: user input → model metadata from `repositories/` → `ecologits` impact calculation → `core/formatting.py` → `ui/impacts.py` display.

**Caching**: model/repo data is loaded with `@st.cache_data` — changes to repository functions need cache invalidation in mind.

## Key dependencies

- `ecologits` — the upstream impact calculation library. Its `Impacts` / `ImpactsOutput` types are used throughout; check its API before assuming attribute names.
- `pint` — unit conversions live in `src/core/units.py`; always go through the unit registry there, don't construct raw `pint` quantities elsewhere.
- `streamlit-aggrid` — used for the company-mode data grid.

## CI/CD

GitHub Actions runs ruff, mypy (non-blocking), and pytest on Python 3.11/3.12. Pushes to `main` auto-deploy to Hugging Face Spaces.
