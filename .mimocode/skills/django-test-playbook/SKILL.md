---
name: django-test-playbook
description: Write pytest-based tests for a Django REST Framework app endpoint. Handles venv discovery, pytest config, fixtures, and migration issues.
---

# Django REST API Test Playbook

Write comprehensive pytest tests for a Django REST Framework app's endpoints.

## When to Use

- User asks to "write tests for [app] endpoints"
- User asks to "add tests for [app]"
- Writing tests for a new or existing DRF app

## Procedure

### 1. Discover Project Structure

```bash
# Find the app directory and key files
ls <app>/
cat <app>/models.py
cat <app>/views.py
cat <app>/urls.py
cat <app>/serializers.py  # if exists
```

### 2. Find Python Virtual Environment

```bash
# Check common venv locations
ls venv/bin/python* .venv/bin/python* env/bin/python* 2>/dev/null
which python3 pytest 2>/dev/null
ls -d venv .venv env 2>/dev/null
```

Store the working python path for all subsequent commands (e.g., `env/bin/python`).

### 3. Check Existing Test Infrastructure

```bash
# Check for existing tests
ls <app>/tests/ 2>/dev/null || ls <app>/tests.py 2>/dev/null
cat pytest.ini
cat conftest.py
```

### 4. Create Test Directory Structure

```bash
# Create tests package if it doesn't exist
mkdir -p <app>/tests
touch <app>/tests/__init__.py
```

### 5. Write conftest.py with Fixtures

Create `<app>/tests/conftest.py` with:
- `api_client` fixture (DRF APIClient)
- `user` fixture (create_user or User.objects.create_user)
- Domain-specific fixtures (e.g., `bootcamp`, `enrollment`) based on model dependencies
- Use `@pytest.fixture` with proper factory patterns

### 6. Write Test File

Create `<app>/tests/test_<feature>.py`:
- Import pytest, reverse, status, models, serializers
- Write test class or function-based tests
- Cover: list, detail, create, update, delete, permissions, filtering
- Use `@pytest.mark.django_db` for database access
- Use `api_client.force_authenticate(user=user)` for authenticated tests

### 7. Update pytest.ini if Needed

```ini
[pytest]
DJANGO_SETTINGS_MODULE = <project>.settings.local
python_files = tests.py test_*.py *_tests.py
addopts = -q
```

### 8. Run Tests

```bash
# Run the specific app's tests
env/bin/python -m pytest <app>/tests/ -v

# If migration errors occur, try:
env/bin/python -m pytest <app>/tests/ --no-migrations -v

# Run full suite to verify no regressions
env/bin/python -m pytest -q
```

### 9. Fix Common Issues

- **ModuleNotFoundError**: Check pytest.ini `DJANGO_SETTINGS_MODULE`
- **Migration errors**: Use `--no-migrations` flag or run `makemigrations` first
- **Import errors**: Verify `__init__.py` exists in tests directory
- **Fixture errors**: Check model field requirements and constraints

## Stopping Condition

All tests pass with `env/bin/python -m pytest <app>/tests/ -v` and full suite passes with `env/bin/python -m pytest -q`.

## Example Flow (from trajectory)

```
ses_0a6324f9dffeF6DDhHtTAmcArs - "write test for enrollments endpoints"
1. Explored enrollment models, views, urls, defaults
2. Created enrollments/tests/ directory
3. Wrote conftest.py with api_client, user, bootcamp fixtures
4. Wrote test_enrollment.py with list, detail, create tests
5. Found venv (env/bin/python)
6. Fixed pytest.ini (added testpaths)
7. Handled migration issues (--no-migrations)
8. Ran full suite successfully
```
