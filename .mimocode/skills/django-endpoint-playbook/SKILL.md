---
name: django-endpoint-playbook
description: Add a model field with full CRUD endpoints (serializer, view, URL, migration) following Django REST Framework conventions.
---

# Django Endpoint Playbook

Add a new field to a Django model and create full CRUD endpoints (serializer, view, URL, migration).

## When to Use

- User asks to "add [field] to [model] and create endpoints"
- User asks to "add serializer and views for [model]"
- User asks to "create list and detail endpoints for [model]"

## Procedure

### 1. Read Existing Model

```bash
cat <app>/models.py
```

Understand the model structure, existing fields, and relationships.

### 2. Explore Project Conventions

```bash
# Check existing patterns
cat <project>/urls.py           # main URL config
cat <app>/urls.py               # app URLs
cat <app>/views.py              # existing views
cat <app>/serializers.py        # if exists
ls <app>/migrations/            # migration history
```

### 3. Add Field to Model

Edit `<app>/models.py`:
- Add the new field with proper type, constraints, and default
- Follow existing field ordering conventions

### 4. Create/Update Serializer

Create or update `<app>/serializers.py`:
- Import model and related models
- Create serializer class with appropriate fields
- Use nested serializers for related objects if needed
- Follow existing serializer patterns in the project

### 5. Create/Update Views

Create or update `<app>/views.py`:
- Use DRF generic views (ListAPIView, RetrieveAPIView, CreateAPIView, etc.)
- Set appropriate permissions (AllowAny, IsAuthenticated, etc.)
- Import serializers and models

### 6. Update URLs

Update `<app>/urls.py`:
- Add URL patterns for new endpoints
- Use descriptive names (e.g., `bootcamp_list`, `bootcamp_detail`)
- Follow existing URL naming conventions

### 7. Generate Migration

```bash
# Find venv first
ls venv/bin/python* .venv/bin/python* env/bin/python* 2>/dev/null

# Generate migration
env/bin/python manage.py makemigrations <app>

# Check for missing dependencies
env/bin/python manage.py makemigrations --check --dry-run
```

### 8. Install Missing Dependencies (if needed)

```bash
# If Pillow or other packages are missing
source env/bin/activate 2>/dev/null
pip install <package>
```

### 9. Run System Check

```bash
env/bin/python manage.py check
```

### 10. Verify

```bash
# Run migration
env/bin/python manage.py migrate

# Run tests if they exist
env/bin/python -m pytest <app>/tests/ -v
```

## Stopping Condition

- Field added to model
- Serializer created
- Views created
- URLs updated
- Migration generated successfully
- `manage.py check` passes with no errors

## Example Flow (from trajectory)

```
ses_0a6324fb1ffeM6s55sGzM1AW6g - "add status field to bootcamp and endpoints"
1. Read courses/models.py (Bootcamp model)
2. Explored project structure (urls, views, serializers, migrations)
3. Added status CharField to Bootcamp model
4. Created courses/serializers.py with BootcampListSerializer, BootcampDetailSerializer
5. Created courses/views.py with BootcampListView, BootcampDetailView
6. Updated courses/urls.py with bootcamp_list, bootcamp_detail URLs
7. Ran makemigrations (hit Pillow dependency, installed it)
8. Ran manage.py check successfully
```
