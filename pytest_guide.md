# The Complete Pytest Guide — From Zero to Advanced

A single-file, end-to-end reference for `pytest`, Python's most popular testing framework. Read it top to bottom if you're new, or jump to a section if you already know the basics.

---

## Table of Contents

1. [What is pytest and why use it](#1-what-is-pytest-and-why-use-it)
2. [Installation and setup](#2-installation-and-setup)
3. [Your first test](#3-your-first-test)
4. [Test discovery rules](#4-test-discovery-rules)
5. [Assertions](#5-assertions)
6. [Running tests (CLI)](#6-running-tests-cli)
7. [Fixtures — the heart of pytest](#7-fixtures--the-heart-of-pytest)
8. [Parametrization](#8-parametrization)
9. [Markers](#9-markers)
10. [conftest.py — sharing fixtures across files](#10-conftestpy--sharing-fixtures-across-files)
11. [Built-in fixtures you should know](#11-built-in-fixtures-you-should-know)
12. [Testing exceptions and warnings](#12-testing-exceptions-and-warnings)
13. [Mocking with pytest](#13-mocking-with-pytest)
14. [Project structure & configuration](#14-project-structure--configuration)
15. [Test coverage](#15-test-coverage)
16. [Parallel test execution](#16-parallel-test-execution)
17. [Async testing](#17-async-testing)
18. [Useful plugins ecosystem](#18-useful-plugins-ecosystem)
19. [Debugging failing tests](#19-debugging-failing-tests)
20. [CI integration](#20-ci-integration)
21. [Best practices & common pitfalls](#21-best-practices--common-pitfalls)
22. [Quick-reference cheatsheet](#22-quick-reference-cheatsheet)

---

## 1. What is pytest and why use it

`pytest` is a testing framework for Python. It lets you write tests as plain functions, using the built-in `assert` keyword, instead of writing verbose classes like the standard library's `unittest` requires.

**Why people prefer it over `unittest`:**

| Feature | `unittest` | `pytest` |
|---|---|---|
| Write a test | Subclass `TestCase` | Plain function |
| Assertions | `self.assertEqual(a, b)` | `assert a == b` |
| Setup/teardown reuse | Inheritance-based | Fixtures (composable) |
| Test parametrization | Manual loops or 3rd-party | Built-in `@pytest.mark.parametrize` |
| Plugin ecosystem | Small | Huge (1000+ plugins) |
| Error output | Basic | Detailed diffs, auto-inspection |

pytest is also fully compatible with existing `unittest`-based tests, so you can adopt it gradually.

---

## 2. Installation and setup

```bash
# Basic install
pip install pytest

# Recommended: install inside a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pytest

# Check version
pytest --version
```

For a real project, pin it in your dependency file:

```
# requirements-dev.txt
pytest>=8.0
pytest-cov>=5.0
pytest-mock>=3.14
```

---

## 3. Your first test

Create a file `test_math.py`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

Run it:

```bash
pytest
```

Output:

```
============================= test session starts ==============================
collected 1 item

test_math.py .                                                             [100%]

============================== 1 passed in 0.01s ===============================
```

That's it. No class, no imports beyond your own code — `pytest` finds and runs the test automatically.

---

## 4. Test discovery rules

pytest finds tests using naming conventions, not decorators or registration. By default:

- **Files**: must match `test_*.py` or `*_test.py`
- **Functions**: must start with `test_`
- **Classes**: must start with `Test` (and must **not** define an `__init__` method)
- **Methods** inside those classes: must start with `test_`

```python
# ✅ Discovered
def test_login():
    ...

class TestUser:
    def test_creation(self):
        ...

# ❌ Not discovered — wrong prefix
def check_login():
    ...

class UserTests:      # doesn't start with "Test"
    def test_creation(self):
        ...
```

You can customize these patterns in `pytest.ini` / `pyproject.toml` (see [Section 14](#14-project-structure--configuration)) but the defaults work for 95% of projects.

---

## 5. Assertions

pytest supercharges Python's plain `assert` statement — no special assertion methods to memorize.

```python
def test_examples():
    assert 1 + 1 == 2
    assert "py" in "pytest"
    assert [1, 2, 3] == [1, 2, 3]
    assert {"a": 1} == {"a": 1}
    assert not False
    assert 5 > 3, "custom failure message shown if this fails"
```

When an assertion **fails**, pytest shows a detailed breakdown (called "assertion rewriting") — you don't need to pick a specific method like `assertEqual` vs `assertIn`:

```python
def test_lists():
    assert [1, 2, 3] == [1, 2, 4]
```

```
E       assert [1, 2, 3] == [1, 2, 4]
E         At index 2 diff: 3 != 4
```

### Approximate comparisons (floats)

```python
import pytest

def test_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

---

## 6. Running tests (CLI)

```bash
pytest                          # run everything discovered from cwd
pytest test_math.py             # run one file
pytest test_math.py::test_add   # run one function
pytest test_math.py::TestUser::test_creation   # run one method in a class

pytest -v                       # verbose — shows each test name
pytest -q                       # quiet — minimal output
pytest -x                       # stop after the first failure
pytest --maxfail=3              # stop after 3 failures
pytest -k "login and not admin" # run tests matching a name expression
pytest -m "slow"                # run tests tagged with a marker (see Section 9)
pytest --lf                     # rerun only tests that failed last time
pytest --ff                     # run failed tests first, then the rest
pytest -s                       # don't capture print() output — show it live
pytest --tb=short                # shorter tracebacks
pytest --collect-only           # list what would run, without running it
```

---

## 7. Fixtures — the heart of pytest

A **fixture** is a function that provides data, a connection, or setup/teardown logic to your tests. It replaces `setUp`/`tearDown` with something more flexible and reusable.

### 7.1 Basic fixture

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Harsh", "role": "developer"}

def test_name(sample_data):
    assert sample_data["name"] == "Harsh"
```

pytest sees that `test_name` has a parameter called `sample_data`, matches it to the fixture with that name, calls the fixture, and injects the return value. No imports, no manual wiring.

### 7.2 Setup and teardown with `yield`

Anything before `yield` runs as setup; anything after runs as teardown (cleanup), even if the test fails.

```python
@pytest.fixture
def db_connection():
    conn = connect_to_test_db()   # setup
    yield conn                    # this is what the test receives
    conn.close()                  # teardown — always runs
```

### 7.3 Fixture scope

By default a fixture runs once **per test**. You can widen that:

```python
@pytest.fixture(scope="function")   # default — runs for every test
@pytest.fixture(scope="class")      # once per test class
@pytest.fixture(scope="module")     # once per file
@pytest.fixture(scope="package")    # once per package/directory
@pytest.fixture(scope="session")    # once for the entire test run
```

```python
@pytest.fixture(scope="session")
def api_client():
    client = create_client()   # expensive to create — do it once
    yield client
    client.close()
```

### 7.4 Fixtures using other fixtures

Fixtures can depend on each other, and pytest resolves the chain automatically.

```python
@pytest.fixture
def user():
    return {"id": 1, "name": "Harsh"}

@pytest.fixture
def logged_in_session(user):
    session = create_session(user)
    yield session
    session.destroy()
```

### 7.5 `autouse` fixtures

Runs automatically for every applicable test, without being requested as a parameter.

```python
@pytest.fixture(autouse=True)
def reset_environment():
    os.environ["ENV"] = "test"
    yield
    os.environ.pop("ENV", None)
```

Use sparingly — implicit behavior can make tests harder to follow.

### 7.6 Parametrized fixtures

A fixture can itself run multiple times with different values, and every test using it will run once per value.

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_engine(request):
    return create_engine(request.param)

def test_connection(db_engine):
    assert db_engine.is_connected()
# This test effectively runs 3 times, once per engine.
```

### 7.7 Factory fixtures (fixture that returns a function)

Useful when a test needs to create multiple objects with different data.

```python
@pytest.fixture
def make_user():
    created = []
    def _make_user(name="default"):
        user = User(name=name)
        created.append(user)
        return user
    yield _make_user
    for u in created:
        u.delete()   # cleanup all created users

def test_two_users(make_user):
    alice = make_user("Alice")
    bob = make_user("Bob")
    assert alice.name != bob.name
```

---

## 8. Parametrization

Instead of copy-pasting near-identical tests, run one test function against many inputs.

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert a + b == expected
```

This produces 4 separate, individually-reportable test cases: `test_add[1-2-3]`, `test_add[0-0-0]`, etc.

### Stacking parametrize (creates a full combination matrix)

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", ["a", "b"])
def test_combo(x, y):
    # runs 4 times: (1,a) (1,b) (2,a) (2,b)
    ...
```

### Giving readable IDs to cases

```python
@pytest.mark.parametrize("value,expected", [
    pytest.param(2, 4, id="double-two"),
    pytest.param(3, 6, id="double-three"),
])
def test_double(value, expected):
    assert value * 2 == expected
```

---

## 9. Markers

Markers tag tests with metadata, which you can then filter on or attach special behavior to.

### Built-in markers

```python
import pytest

@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    ...

@pytest.mark.skipif(sys.platform == "win32", reason="unix only")
def test_symlinks():
    ...

@pytest.mark.xfail(reason="known bug, tracked in JIRA-123")
def test_known_bug():
    assert broken_function() == 1

@pytest.mark.xfail(strict=True)  # fails the suite if it unexpectedly PASSES
def test_must_still_be_broken():
    ...
```

### Custom markers

```python
@pytest.mark.slow
def test_large_batch_import():
    ...

@pytest.mark.smoke
def test_health_check():
    ...
```

Register custom markers in `pytest.ini` (otherwise pytest prints a warning):

```ini
[pytest]
markers =
    slow: marks tests as slow-running
    smoke: quick sanity checks
```

Run only marked tests:

```bash
pytest -m slow
pytest -m "smoke and not slow"
```

---

## 10. conftest.py — sharing fixtures across files

`conftest.py` is a special file pytest auto-loads — you never import it. Fixtures and hooks defined there are available to every test in that directory and subdirectories, with no import statement needed.

```
project/
├── conftest.py          # fixtures shared by ALL tests
├── tests/
│   ├── conftest.py       # fixtures shared by tests in this folder only
│   ├── test_api.py
│   └── test_models.py
```

```python
# conftest.py
import pytest

@pytest.fixture
def api_client():
    return APIClient(base_url="http://localhost:8000")
```

Any test anywhere below that `conftest.py` can just do:

```python
def test_get_users(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
```

---

## 11. Built-in fixtures you should know

pytest ships with several ready-made fixtures — no installation needed.

| Fixture | Purpose |
|---|---|
| `tmp_path` | A unique temporary directory (`pathlib.Path`) per test |
| `tmp_path_factory` | Create multiple temp dirs, session-scoped |
| `monkeypatch` | Safely modify env vars, attributes, dict entries — auto-reverted after the test |
| `capsys` | Capture `stdout`/`stderr` |
| `caplog` | Capture and assert on log messages |
| `request` | Introspect the currently running test (name, params, etc.) |

```python
def test_write_file(tmp_path):
    file = tmp_path / "output.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

def test_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-123")
    assert os.environ["API_KEY"] == "test-123"

def test_output(capsys):
    print("hello world")
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"

def test_logging(caplog):
    logger.warning("something happened")
    assert "something happened" in caplog.text
```

---

## 12. Testing exceptions and warnings

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="divide by zero"):
        divide(10, 0)

def test_warning():
    with pytest.deprecated_call():
        old_deprecated_function()
```

You can also inspect the captured exception:

```python
def test_exception_details():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "zero" in str(exc_info.value)
```

---

## 13. Mocking with pytest

Real dependencies (databases, APIs, file systems) are slow and unreliable in tests — mock them out.

### Using the standard library `unittest.mock`

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_service = Mock()
    mock_service.get_price.return_value = 99.99
    assert mock_service.get_price("item-1") == 99.99

@patch("myapp.services.requests.get")
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = call_external_api()
    assert result["status"] == "ok"
```

### Using `pytest-mock` (cleaner syntax, auto-cleanup)

```bash
pip install pytest-mock
```

```python
def test_api_call(mocker):
    mock_get = mocker.patch("myapp.services.requests.get")
    mock_get.return_value.status_code = 200
    result = call_external_api()
    assert result is not None
```

`pytest-mock`'s `mocker` fixture is just a thin, auto-cleaning wrapper around `unittest.mock.patch` — no manual `@patch` decorator stacking required.

---

## 14. Project structure & configuration

### Recommended layout

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── conftest.py
│   ├── test_core.py
│   └── unit/
│       └── test_helpers.py
├── pyproject.toml
└── pytest.ini            # or config inside pyproject.toml
```

### Configuration via `pyproject.toml` (modern, preferred)

```toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```

### Or via `pytest.ini`

```ini
[pytest]
minversion = 8.0
addopts = -ra -q
testpaths = tests
```

`addopts` lets you bake in flags so you never have to type them manually (e.g. `-ra` shows a summary of all non-passing tests at the end).

---

## 15. Test coverage

```bash
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

Output shows which lines were **not** exercised by any test:

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/core.py             42      3    93%   17-19
--------------------------------------------------
TOTAL                    42      3    93%
```

Generate an HTML report you can browse:

```bash
pytest --cov=src --cov-report=html
# open htmlcov/index.html
```

Set a minimum threshold (useful in CI to fail the build if coverage drops):

```bash
pytest --cov=src --cov-fail-under=80
```

---

## 16. Parallel test execution

```bash
pip install pytest-xdist
pytest -n auto     # use all available CPU cores
pytest -n 4         # use exactly 4 workers
```

Speeds up large suites significantly, but be aware: tests must be independent of each other (no shared mutable state, no assumptions about execution order) for this to be safe.

---

## 17. Async testing

For `async def` test functions (common in projects using `asyncio`, `httpx`, `FastAPI`, etc.):

```bash
pip install pytest-asyncio
```

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data()
    assert result is not None
```

To avoid marking every test individually, set a mode in config:

```ini
[pytest]
asyncio_mode = auto
```

With `auto` mode, any `async def test_...` function is automatically treated as an async test — no decorator needed.

---

## 18. Useful plugins ecosystem

pytest's biggest strength is its plugin ecosystem. A few worth knowing:

| Plugin | What it does |
|---|---|
| `pytest-cov` | Code coverage reporting |
| `pytest-mock` | Cleaner mocking via the `mocker` fixture |
| `pytest-xdist` | Parallel/distributed test execution |
| `pytest-asyncio` | Support for `async def` tests |
| `pytest-django` | Django-specific fixtures (`client`, DB rollback per test, etc.) |
| `pytest-playwright` | Browser automation / E2E testing fixtures (`page`, `browser`, `context`) integrated directly into pytest |
| `pytest-timeout` | Fail a test if it runs too long |
| `pytest-rerunfailures` | Automatically retry flaky tests |
| `pytest-sugar` | Prettier, more visual progress output |
| `pytest-randomly` | Randomizes test order to catch hidden inter-test dependencies |
| `pytest-html` | Generates a self-contained HTML test report |
| `faker` | Generates realistic fake data for tests (not a pytest plugin itself, but pairs well) |

If you're already doing Playwright-based E2E work, `pytest-playwright` is worth a look — it gives you `page`/`browser`/`context` as regular pytest fixtures instead of manual setup/teardown.

---

## 19. Debugging failing tests

```bash
pytest --pdb              # drop into the debugger at the point of failure
pytest --trace             # drop into the debugger at the start of every test
pytest -l                  # show local variables in tracebacks
pytest --tb=long           # full traceback (default)
pytest --tb=short          # condensed traceback
pytest --tb=line           # one line per failure
pytest -x --pdb            # stop at first failure and debug it immediately
```

Inside `--pdb`, standard debugger commands apply: `n` (next), `s` (step in), `c` (continue), `p variable_name` (print), `q` (quit).

---

## 20. CI integration

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v4
```

Key flags for CI specifically:

```bash
pytest --tb=short -q --cov=src --cov-fail-under=80 --maxfail=5
```

---

## 21. Best practices & common pitfalls

**Do:**
- Keep each test focused on **one** behavior — if the name needs "and" in it, split it.
- Prefer fixtures over global setup — they're explicit about what each test needs.
- Use `tmp_path` instead of writing to real disk locations.
- Name tests descriptively: `test_login_fails_with_wrong_password`, not `test_1`.
- Keep unit tests fast; mark slow/integration tests separately so they can be skipped in quick local runs.

**Avoid:**
- Tests that depend on execution order or shared mutable global state.
- Overusing `autouse=True` — it hides what a test actually depends on.
- Asserting too much in one test — a failure should point at one clear cause.
- Mocking things you don't own deep inside third-party internals — mock at the boundary of your own code instead.
- Ignoring flaky tests — fix them or explicitly quarantine with `pytest-rerunfailures`, don't just re-run CI until it's green.

**Common gotchas:**
- Fixture not found → check spelling and that it's visible (same file, or a `conftest.py` in an ancestor directory).
- `assert` doesn't show useful info → make sure you're running raw `pytest`, not a wrapped script that strips assertion rewriting.
- Parametrized test IDs look ugly → add `ids=[...]` or use `pytest.param(..., id="...")`.
- Session-scoped fixture behaving unexpectedly across tests → remember it's created once and shared; don't mutate it destructively.

---

## 22. Quick-reference cheatsheet

```bash
# Running
pytest                          # run all tests
pytest path/to/test_file.py     # run one file
pytest -k "expr"                # run tests matching name expression
pytest -m marker_name            # run tests with a marker
pytest -x                       # stop at first failure
pytest --lf                     # rerun last failures only
pytest -n auto                  # parallel run (needs pytest-xdist)

# Fixtures
@pytest.fixture
@pytest.fixture(scope="session")
@pytest.fixture(autouse=True)
@pytest.fixture(params=[...])

# Parametrize
@pytest.mark.parametrize("a,b,expected", [(1,1,2), (2,2,4)])

# Markers
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="...")

# Assertions
assert x == y
pytest.approx(0.3)
with pytest.raises(ValueError, match="pattern"):

# Built-in fixtures
tmp_path, monkeypatch, capsys, caplog, request

# Coverage
pytest --cov=src --cov-report=term-missing
```

---

### Where to go next

- Official docs: https://docs.pytest.org
- Try converting one small existing `unittest` suite of yours into pytest style — it's usually a 20-minute exercise and makes the concepts click fast.
- Once comfortable, explore `pytest-playwright` if your work involves browser E2E testing — it plugs Playwright fixtures directly into everything covered above.
