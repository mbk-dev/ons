# ons — Development rules for AI agents

## What is this

Python client for the UK Office for National Statistics (ONS) API. Fetches macroeconomic data (GDP, CPIH inflation) as pandas Series/DataFrames.

## Environment

- Poetry for environment & dependency management.
- `poetry run python ...` to run scripts.
- `poetry add` instead of `pip install`.

## Test-Driven Development (TDD)

Any change to production code (new feature, bugfix, refactor, behavior change) must follow TDD: **write a failing test first, then the minimal code that makes it pass**.

Cycle: **RED → verify RED → GREEN → verify GREEN → REFACTOR**.

Rules:
- Tests run via: `poetry run pytest -q`.
- Before writing code, see the test fail for a real reason (`AssertionError` / missing function), not a typo/import error.
- For bugfix: first a test reproducing the bug, then the fix.
- One test = one behavior. Test name describes the behavior meaningfully.
- After GREEN, run the full test suite to make sure nothing broke.

## Post-change checklist

1. Determine whether *executable Python code* was changed.
2. If executable code was changed — run tests: `poetry run pytest -q`.
3. If only comments or docstrings were changed — do not run tests.
4. If tests fail, attempt to fix and re-run (max 2 retries), then stop and report.
5. Before finishing any code change, run `poetry run ruff check .` and fix every reported issue. If a warning is truly unavoidable, silence it with a targeted `# noqa: <CODE>` comment.

## ONS API reference

У ONS два публичных API. Оба без аутентификации.

### 1. Website API (используется для CPIH)

Base URL: `https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/{CDID}/{dataset}/data`

Возвращает JSON с массивами `months`, `quarters`, `years`. Данные актуальные (обновляются вместе с сайтом ONS).

Используемые серии:

| CDID | Описание | Единица | Dataset |
|------|----------|---------|---------|
| **L522** | CPIH INDEX 00: ALL ITEMS 2015=100 | Index | mm23 |
| **L55O** | CPIH ANNUAL RATE 00: ALL ITEMS | % | mm23 |
| **D7BT** | CPI INDEX 00: ALL ITEMS 2015=100 | Index | mm23 |

Workflow: `GET .../timeseries/l522/mm23/data` → парсить `response["months"]`, каждый элемент: `{"date": "2026 APR", "value": "141.8"}`.

### 2. Beta API (используется для GDP; ранее использовался для CPIH)

Base URL: `https://api.beta.ons.gov.uk/v1/`

Ответы JSON. CSV — по ссылкам из метаданных версии.

| Endpoint | Description |
|----------|-------------|
| `/datasets/{id}` | Метаданные датасета (title, contacts, editions) |
| `/datasets/{id}/editions` | Доступные editions (обычно `time-series`) |
| `/datasets/{id}/editions/{edition}/versions/{ver}` | Метаданные версии: dimensions, download links (CSV/XLS) |
| `/datasets/{id}/editions/{edition}/versions/{ver}/observations?dim=val&...` | Фильтрованные наблюдения. `*` — wildcard (макс. 10 000 строк) |

Workflow: `GET /datasets/{id}` → `links.latest_version.href` → `downloads.csv.href` → pandas.

#### Beta API: датасеты

**cpih01** — CPIH (ранее использовался в `get_cpih()`, заменён на Website API 2026-05-27)
- Edition: `time-series`, последняя версия в API: 67 (от 2026-02-18, данные по январь 2026)
- Dimensions: `Time` (mmm-yy), `Geography` (uk-only), `Aggregate` (cpih1dim1aggid)
- Фильтр: `Aggregate == 'Overall Index'`
- Проблема: API перестал обновляться с февраля 2026, сайт ONS уходит вперёд на месяцы
- Для возврата: в `infl.py` заменить вызов `get_timeseries("l522")` обратно на `get_data("cpih01")` и парсить CSV через `pd.read_csv(StringIO(response))` с фильтром по `Aggregate`
- Docs: https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/consumerpriceinflation
- API explorer: https://developer.ons.gov.uk/observations/

**regional-gdp-by-quarter** — Quarterly GDP for England, Wales and English regions
- Edition: `time-series`, latest version: 6
- Dimensions: `Time` (yyyy-qq), `Geography` (nuts), `sic-unofficial` (SIC codes), `type-of-prices`, `quarterly-index-and-growth-rate`
- Фильтр: `nuts == 'UK0'`, `sic-unofficial == 'A--T'`, `GrowthRate == 'Quarterly index'`
- Last updated: 2023-05-24
- Contact: regionalgdp@ons.gov.uk

## Project structure

- `ons/` — library source code
  - `request_data.py` — HTTP client (Website API + Beta API)
  - `gdp.py` — UK GDP quarterly index
  - `infl.py` — CPIH index and inflation rate
- `tests/` — pytest test suite
- `main.py` — usage examples

## Python style

- All code comments and docstrings in **English**.
- Type hints for all function parameters and return types.
- Minimum supported Python version: see `pyproject.toml` (`python = ">=3.14,<4.0.0"`).
- Use modern syntax: built-in generics (`list[int]`), union syntax (`X | None`), literals over constructors.
- **Ruff configuration** is in `pyproject.toml` (`[tool.ruff.lint]`, selecting `C,E,F,W,B`). Treat it as the authoritative style guide.
