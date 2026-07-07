<div align="center">
  <h1>🍽️🛍️ Visika</h1>
  <p><strong>A Modern, Production-Ready B2B Food Marketplace Backend</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Django-6.0-092E20.svg?logo=django" alt="Django Version" />
    <img src="https://img.shields.io/badge/DRF-3.16-red.svg" alt="DRF Version" />
    <img src="https://img.shields.io/badge/Database-PostgreSQL-336791.svg?logo=postgresql" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Cache-Redis-DC382D.svg?logo=redis" alt="Redis" />
    <img src="https://img.shields.io/badge/Task_Queue-Celery-37814A.svg?logo=celery" alt="Celery" />
  </p>
</div>

<hr>

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Architecture & Features](#-architecture--features)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Docker Setup (Recommended)](#docker-setup-recommended)
  - [Local Setup (Bare Metal)](#local-setup-bare-metal)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [License](#-license)

---

## 🚀 About the Project

**Visika** is the backend infrastructure for a cutting-edge B2B food marketplace. Designed with scalability, security, and maintainability in mind, it leverages a modernized Django stack to handle complex business logic, background task processing, and secure authentication flows.

---

## ✨ Architecture & Features

- **Decoupled Settings**: Environment-specific settings (`base.py`, `local.py`, `prod.py`) powered by `django-environ`.
- **Secure Authentication**: JWT tokens stored securely in HTTP-only cookies with stringent **CSRF enforcement**.
- **OTP Login Flow**: OTP via SMS integration (Faraz SMS) using strict DRF Throttling to prevent SMS bombing.
- **Service Layer Pattern**: Business logic decoupled from Views into reusable, testable Services.
- **Background Tasks**: Asynchronous processing with Celery & Redis, featuring robust exponential retry mechanisms for external network calls.
- **Standardized Error Handling**: Unified JSON exception responses across the entire API layer.
- **Dockerized**: Complete container parity across development and production environments.

---

## 🛠️ Getting Started

### Prerequisites

* [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) (For Docker deployment)
* Python 3.11+ (For local deployment)
* PostgreSQL & Redis (For local deployment)

### Environment Variables

Create a `.env` file in the root of the project. Here is a starter template:

```env
# Core Django
DEBUG=True
SECRET_KEY=your-super-secure-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
DJANGO_SETTINGS_MODULE=visika.settings.local

# Database (For Docker / Postgres Setup)
DATABASE_URL=postgres://visika_user:visika_password@db:5432/visika

# Redis / Celery
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Faraz SMS Provider
FARAZ_SMS_API_KEY=your_actual_api_key_here
FARAZ_SMS_SENDER_NUMBER=3000xxxxxx
FARAZ_SMS_LOGIN_OTP_PATTERN_CODE=your_pattern_code
```

---

### 🐳 Docker Setup (Recommended)

The easiest way to get the project up and running is via Docker. This setup includes the Django web server, PostgreSQL database, Redis cache, and a Celery worker.

1. Build and spin up the containers:
   ```bash
   docker-compose up --build
   ```
2. Run database migrations inside the container:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

*The API will be available at `http://localhost:8000`.*

---

### 💻 Local Setup (Bare Metal)

If you prefer running the project locally without Docker (e.g., using SQLite for fast iteration):

1. **Set Local Environment:**
   Ensure your `.env` contains:
   ```env
   DJANGO_SETTINGS_MODULE=visika.settings.local
   # SQLite will be used automatically when running locally without a DATABASE_URL.
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements/local.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start Services:**
   You will need to start the web server and the celery worker in separate terminal windows.
   
   *Web Server:*
   ```bash
   python manage.py runserver
   ```
   
   *Celery Worker:*
   ```bash
   celery -A visika worker --loglevel=INFO
   ```

---

## 📂 Project Structure

```text
visika_backend/
│
├── core/                   # Base models, custom exception handlers, abstract logic
├── users/                  # User models, OTP auth flows, services layer, tasks
├── visika/                 # Core project configuration
│   └── settings/           # Splitted settings (base, local, prod)
├── third_parties/          # External integrations (e.g., Faraz SMS provider)
├── requirements/           # Segregated dependency lists (base, local, prod)
│
├── Dockerfile              # Production-ready Docker configuration
├── docker-compose.yml      # Multi-container orchestration
└── manage.py               # Django management script
```

---

## 🧪 Testing

The project uses `pytest` for unit and integration testing.

To run the test suite:
```bash
pytest
```

To run with coverage:
```bash
pytest --cov=.
```

---

## 📚 API Documentation

Currently, endpoints can be explored via Postman or cURL.
*(Note: Swagger/Redoc integration can be accessed at `/swagger/` if `drf-yasg` or `drf-spectacular` is added to the installed apps.)*

### Core Endpoints

* **POST** `/users/signup/` - Register a new user
* **POST** `/users/otp/request/` - Request an OTP via SMS
* **POST** `/users/otp/login/` - Validate OTP and receive HttpOnly JWT Cookies
* **GET** `/users/info/` - Fetch current user profile (Requires Auth)
* **POST** `/users/refresh/` - Refresh the access token

---

<div align="center">
  <p>Developed with ❤️ by <strong>Ramin👑</strong></p>
</div>
