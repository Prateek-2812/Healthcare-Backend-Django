# Healthcare Backend — Django + DRF + PostgreSQL + JWT

A full-stack healthcare management system with REST APIs and a browser-based frontend.

---

## Table of Contents

1. [Tech Stack](#tech-stack)  
2. [Project Structure](#project-structure)  
3. [Prerequisites](#prerequisites)  
4. [Database Setup (PostgreSQL)](#database-setup-postgresql)  
5. [Project Setup (Step-by-Step)](#project-setup-step-by-step)  
6. [Running the Server](#running-the-server)  
7. [Seed Data & Login Credentials](#seed-data--login-credentials)  
8. [Frontend Pages](#frontend-pages)  
9. [API Reference](#api-reference)  
10. [API Usage Examples (curl)](#api-usage-examples-curl)  
11. [Environment Variables](#environment-variables)  
12. [Admin Panel](#admin-panel)  
13. [Troubleshooting](#troubleshooting)  

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend framework | Django 6.0.2 |
| REST API | Django REST Framework 3.16.1 |
| Authentication | JWT via `djangorestframework-simplejwt` 5.5.1 |
| Database | PostgreSQL (via `psycopg2-binary`) |
| Env variables | `python-dotenv` |
| Frontend | Django Templates + Vanilla JavaScript + CSS |

---

## Project Structure

```
Healthcare Backend-Django/
├── manage.py
├── requirements.txt
├── .env                          # Your local env vars (git-ignored)
├── .env.example                  # Template for .env
├── .gitignore
├── README.md                     # ← You are here
│
├── healthcare_backend/           # Django project config
│   ├── settings.py               # INSTALLED_APPS, DB, JWT, DRF config
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                     # Auth app (register + login)
│   ├── serializers.py            # RegisterSerializer, LoginSerializer
│   ├── views.py                  # RegisterView, LoginView (AllowAny)
│   └── urls.py                   # /api/auth/register/, /api/auth/login/
│
├── patients/                     # Patient CRUD app
│   ├── models.py                 # Patient model (FK → User)
│   ├── serializers.py            # PatientSerializer
│   ├── views.py                  # List/Create + Detail (user-scoped)
│   ├── urls.py                   # /api/patients/, /api/patients/<id>/
│   ├── admin.py                  # PatientAdmin
│   └── management/
│       └── commands/
│           └── seed_data.py      # python manage.py seed_data
│
├── doctors/                      # Doctor CRUD app
│   ├── models.py                 # Doctor model (FK → User)
│   ├── serializers.py            # DoctorSerializer
│   ├── views.py                  # List/Create + Detail (global)
│   ├── urls.py                   # /api/doctors/, /api/doctors/<id>/
│   └── admin.py                  # DoctorAdmin
│
├── mappings/                     # Patient↔Doctor mapping app
│   ├── models.py                 # PatientDoctorMapping (unique_together)
│   ├── serializers.py            # MappingSerializer, MappingDetailSerializer
│   ├── views.py                  # List/Create, ByPatient, Delete
│   ├── urls.py                   # /api/mappings/, /api/mappings/<id>/, ...
│   └── admin.py                  # MappingAdmin
│
├── frontend/                     # Browser-based UI
│   ├── views.py                  # Template-rendering views
│   ├── urls.py                   # /, /login/, /register/, /dashboard/, etc.
│   ├── static/frontend/
│   │   ├── css/style.css         # Full stylesheet
│   │   └── js/app.js             # JWT-based API helper + utilities
│   └── templates/frontend/
│       ├── base.html             # Base template (auth pages)
│       ├── app_base.html         # App template (navbar + auth guard)
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── patients.html
│       ├── doctors.html
│       └── mappings.html
│
└── core/                         # ⚠️ OLD app (no longer used)
    └── ...                       # Can be safely deleted
```

> **Note:** The `core/` folder is the original single-app structure. It is **not included** in `INSTALLED_APPS` and is completely unused. You can safely delete it with `rm -rf core/`.

---

## Prerequisites

| Tool | Version | Check command |
|------|---------|---------------|
| Python | 3.10+ | `python3 --version` |
| pip | any | `pip --version` |
| PostgreSQL | 14+ | `psql --version` |

On Mac, the easiest way to get PostgreSQL is [**Postgres.app**](https://postgresapp.com).

---

## Database Setup (PostgreSQL)

### Using Postgres.app (Mac)

1. Open **Postgres.app** → ensure server is **Running**.
2. Open Terminal and connect as the default superuser:

```bash
psql -h localhost -p 5432 -U postgres
```

3. Run the following SQL commands:

```sql
-- Create database
CREATE DATABASE healthcare_db;

-- Create app user (skip if already exists)
CREATE USER healthcare_user WITH PASSWORD 'healthcare_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;

-- Connect to the new DB and grant schema access (PostgreSQL 15+ requires this)
\c healthcare_db
GRANT ALL ON SCHEMA public TO healthcare_user;

-- Exit
\q
```

### Verify connection

```bash
psql -h localhost -p 5432 -U healthcare_user -d healthcare_db
# Type \q to exit
```

---

## Project Setup (Step-by-Step)

```bash
# 1. Navigate to project
cd "/Users/prateeksingh/Documents/Healthcare Backend-Django"

# 2. Create virtual environment (skip if venv/ already exists)
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env if your DB credentials differ from defaults

# 6. Generate migration files for all apps
python manage.py makemigrations accounts patients doctors mappings

# 7. Apply migrations to database
python manage.py migrate

# 8. Seed database with demo data (3 users, 8 doctors, 10 patients, 14 mappings)
python manage.py seed_data

# 9. (Optional) Create a Django superuser for /admin/ panel
python manage.py createsuperuser

# 10. Start the development server
python manage.py runserver
```

---

## Running the Server

```bash
cd "/Users/prateeksingh/Documents/Healthcare Backend-Django"
source venv/bin/activate
python manage.py runserver
```

Server starts at: **http://127.0.0.1:8000/**

---

## Seed Data & Login Credentials

Run `python manage.py seed_data` to populate the database. This creates:

| Entity | Count |
|--------|-------|
| Users | 3 |
| Doctors | 8 (Cardiology, Dermatology, Orthopedics, Pediatrics, Neurology, Ophthalmology, General Medicine, Gynecology) |
| Patients | 10 (with realistic medical histories) |
| Mappings | 14 (pre-assigned doctor-patient relationships) |

### Login Credentials

> **⚠️ The login page uses EMAIL, not username.**

| Email | Password | Username |
|-------|----------|----------|
| `admin@healthcare.com` | `Admin@1234` | dr_admin |
| `jane@healthcare.com` | `Jane@1234` | nurse_jane |
| `bob@healthcare.com` | `Bob@12345` | receptionist_bob |

---

## Frontend Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Redirects to `/login/` |
| Login | `/login/` | Email + password → JWT login |
| Register | `/register/` | Create account (username, email, password) |
| Dashboard | `/dashboard/` | Stats overview (patients/doctors/assignments count) + quick action cards |
| Patients | `/patients/` | CRUD table with Add/Edit modal and Delete button |
| Doctors | `/doctors/` | CRUD table with Add/Edit modal and Delete button |
| Mappings | `/mappings/` | Assign doctor↔patient via dropdowns + view/remove assignments |

### Frontend Flow

```
/login/ (or /register/)
   │
   ▼  (JWT token stored in localStorage)
/dashboard/
   │
   ├──→ /patients/   (manage your patients)
   ├──→ /doctors/    (manage all doctors)
   └──→ /mappings/   (assign doctors to patients)
```

- The navbar has links to all pages + a **Logout** button
- Pages are **auth-guarded**: if no JWT token is found, you're redirected to `/login/`
- All API calls include `Authorization: Bearer <token>` header automatically

---

## API Reference

### Base URL: `http://127.0.0.1:8000/api`

### Authentication APIs (no token needed)

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|----------|
| `POST` | `/api/auth/register/` | `{ "username", "email", "password" }` | `201` with user info |
| `POST` | `/api/auth/login/` | `{ "email", "password" }` | `200` with `tokens.access` and `tokens.refresh` |

### Patient APIs (token required, scoped to your user)

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|----------|
| `GET` | `/api/patients/` | — | `200` list of YOUR patients |
| `POST` | `/api/patients/` | `{ "name", "age", "gender", "phone", "address", "medical_history" }` | `201` created patient |
| `GET` | `/api/patients/<id>/` | — | `200` patient detail |
| `PUT` | `/api/patients/<id>/` | full patient object | `200` updated patient |
| `DELETE` | `/api/patients/<id>/` | — | `204` deleted |

### Doctor APIs (token required, global access)

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|----------|
| `GET` | `/api/doctors/` | — | `200` list of ALL doctors |
| `POST` | `/api/doctors/` | `{ "name", "specialization", "phone", "email", "experience_years" }` | `201` created doctor |
| `GET` | `/api/doctors/<id>/` | — | `200` doctor detail |
| `PUT` | `/api/doctors/<id>/` | full doctor object | `200` updated doctor |
| `DELETE` | `/api/doctors/<id>/` | — | `204` deleted |

### Mapping APIs (token required)

| Method | Endpoint | Request Body | Response |
|--------|----------|-------------|----------|
| `GET` | `/api/mappings/` | — | `200` all mappings (with nested patient & doctor data) |
| `POST` | `/api/mappings/` | `{ "patient": <id>, "doctor": <id> }` | `201` mapping created |
| `GET` | `/api/mappings/patient/<patient_id>/` | — | `200` doctors assigned to that patient |
| `DELETE` | `/api/mappings/<id>/` | — | `204` mapping removed |

### Authentication Header

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

JWT token lifetime:
- **Access token:** 1 hour
- **Refresh token:** 7 days

---

## API Usage Examples (curl)

### 1. Register a new user

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "Test@1234"}'
```

### 2. Login and get JWT token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@healthcare.com", "password": "Admin@1234"}'
```

Response:
```json
{
  "message": "Login successful.",
  "tokens": {
    "access": "eyJ0eXAi...",
    "refresh": "eyJ0eXAi..."
  }
}
```

### 3. List your patients (using the access token)

```bash
curl http://127.0.0.1:8000/api/patients/ \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### 4. Add a new patient

```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "Content-Type: application/json" \
  -d '{"name": "New Patient", "age": 30, "gender": "Male", "phone": "+91-9999999999"}'
```

### 5. Assign a doctor to a patient

```bash
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Authorization: Bearer eyJ0eXAi..." \
  -H "Content-Type: application/json" \
  -d '{"patient": 1, "doctor": 2}'
```

### 6. Get doctors assigned to patient #1

```bash
curl http://127.0.0.1:8000/api/mappings/patient/1/ \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### 7. Delete a mapping

```bash
curl -X DELETE http://127.0.0.1:8000/api/mappings/5/ \
  -H "Authorization: Bearer eyJ0eXAi..."
```

---

## Environment Variables

Stored in `.env` (git-ignored). Copy from `.env.example`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | `django-insecure-dev-key` | **Change this** in production |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated allowed hosts |
| `POSTGRES_DB` | `healthcare_db` | PostgreSQL database name |
| `POSTGRES_USER` | `healthcare_user` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `password` | PostgreSQL password |
| `POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |

---

## Admin Panel

Access at: **http://127.0.0.1:8000/admin/**

Use a superuser account (created via `python manage.py createsuperuser`) to manage:
- **Patients** — list, search by name, filter by gender
- **Doctors** — list, search by name/specialization, filter by specialization
- **Patient-Doctor Mappings** — list, search by patient/doctor name

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'django'` | Run `source venv/bin/activate` then `pip install -r requirements.txt` |
| `FATAL: database "healthcare_db" does not exist` | Create the database — see [Database Setup](#database-setup-postgresql) |
| `FATAL: role "healthcare_user" does not exist` | Create the user — see [Database Setup](#database-setup-postgresql) |
| `FATAL: password authentication failed` | Check your `.env` file matches the password you set in PostgreSQL |
| `permission denied for schema public` | Run `GRANT ALL ON SCHEMA public TO healthcare_user;` inside `psql` (connected to `healthcare_db`) |
| `No migrations to apply` | Migrations are already applied. This is fine. |
| Login says "Invalid email or password" | Use **email** (e.g. `admin@healthcare.com`), not username |
| 401 Unauthorized on API calls | Your JWT token may have expired (1hr). Login again to get a new one. |
| `relation "patients_patient" does not exist` | Run `python manage.py makemigrations && python manage.py migrate` |
