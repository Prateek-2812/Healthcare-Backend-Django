# Django Assignment: Healthcare Backend

**Submitted by:** Prateek Singh  
**Date:** 26 February 2026  
**GitHub Repository:** [Healthcare-Backend-Django](https://github.com/Prateek-2812/Healthcare-Backend-Django)

---

## 1. Objective

Built a full-stack healthcare backend system using Django, Django REST Framework, and PostgreSQL. The application allows users to register, log in (via JWT), and manage patient and doctor records securely through RESTful APIs. A browser-based frontend (Django templates + vanilla JS) is also provided.

---

## 2. Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend Framework | Django | 6.0.2 |
| REST API | Django REST Framework | 3.16.1 |
| Authentication | djangorestframework-simplejwt | 5.5.1 |
| Database | PostgreSQL | 18.x |
| DB Adapter | psycopg2-binary | 2.9.11 |
| Environment Config | python-dotenv | 1.2.1 |
| Frontend | Django Templates + Vanilla JavaScript + CSS | — |

---

## 3. Project Architecture

The project follows a **modular multi-app architecture**, separating concerns into distinct Django apps:

```
Healthcare Backend-Django/
├── accounts/          # Authentication (register, login, JWT)
├── patients/          # Patient CRUD (user-scoped)
├── doctors/           # Doctor CRUD (global access)
├── mappings/          # Patient↔Doctor relationships
├── frontend/          # Browser UI (templates + static assets)
├── healthcare_backend/ # Project-level settings & URL routing
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

### Design Decisions

- **Separate apps per entity** — Each domain (accounts, patients, doctors, mappings) has its own models, serializers, views, and URL config for clean separation of concerns.
- **JWT Authentication** — All protected API endpoints require a Bearer token. Access tokens expire in 1 hour; refresh tokens in 7 days.
- **User-scoped patients** — Patients are tied to the user who created them (`ForeignKey → User`), so each user only sees their own patients.
- **Global doctor access** — All authenticated users can view and manage the shared doctors pool.
- **Environment variables** — Sensitive config (DB credentials, secret key) loaded from `.env` via `python-dotenv`.

---

## 4. Database Schema

```
┌──────────────┐       ┌──────────────┐
│   User       │       │   Doctor     │
│ (auth_user)  │       │              │
│──────────────│       │──────────────│
│ id           │       │ id           │
│ username     │       │ name         │
│ email        │       │ specialization│
│ password     │       │ phone        │
│              │       │ email        │
│              │       │ experience   │
│              │       │ created_by → User │
└──────┬───────┘       └──────┬───────┘
       │                      │
       │ FK                   │ FK
       ▼                      │
┌──────────────┐              │
│   Patient    │              │
│──────────────│              │
│ id           │              │
│ name         │              │
│ age          │              │
│ gender       │              │
│ phone        │              │
│ address      │              │
│ medical_history│            │
│ created_by → User │         │
└──────┬───────┘              │
       │                      │
       │ FK                   │ FK
       ▼                      ▼
┌─────────────────────────────────┐
│   PatientDoctorMapping          │
│─────────────────────────────────│
│ id                              │
│ patient → Patient               │
│ doctor  → Doctor                │
│ created_at                      │
│ UNIQUE(patient, doctor)         │
└─────────────────────────────────┘
```

---

## 5. API Endpoints Implemented

### Authentication (No token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register with username, email, password |
| `POST` | `/api/auth/login/` | Login with email + password → returns JWT access & refresh tokens |

### Patient Management (Token required, user-scoped)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/patients/` | List patients created by the logged-in user |
| `POST` | `/api/patients/` | Create a new patient |
| `GET` | `/api/patients/<id>/` | Retrieve a specific patient |
| `PUT` | `/api/patients/<id>/` | Update a patient |
| `DELETE` | `/api/patients/<id>/` | Delete a patient |

### Doctor Management (Token required, global)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/doctors/` | List all doctors |
| `POST` | `/api/doctors/` | Add a new doctor |
| `GET` | `/api/doctors/<id>/` | Retrieve a specific doctor |
| `PUT` | `/api/doctors/<id>/` | Update a doctor |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor Mapping (Token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/mappings/` | List all mappings |
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/patient/<patient_id>/` | Get all doctors assigned to a patient |
| `DELETE` | `/api/mappings/<id>/` | Remove a mapping |

### Authentication Header Format

```
Authorization: Bearer <access_token>
```

---

## 6. Key Implementation Details

### JWT Configuration

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Error Handling & Validation

- **Registration:** Validates unique email, enforces password requirements
- **Login:** Returns descriptive error for invalid credentials
- **Patient/Doctor CRUD:** Returns 404 for non-existent records, 400 for validation errors
- **Mappings:** Enforces `unique_together` constraint — prevents duplicate doctor-patient assignments
- **All protected routes:** Return 401 for missing/expired tokens

### Seed Data Command

A management command (`python manage.py seed_data`) populates the database with:

| Entity | Count |
|--------|-------|
| Users | 3 |
| Doctors | 8 (across specializations) |
| Patients | 10 (with medical histories) |
| Mappings | 14 (pre-assigned relationships) |

---

## 7. Frontend

A complete browser-based UI was built using Django templates and vanilla JavaScript:

| Page | Route | Functionality |
|------|-------|---------------|
| Login | `/login/` | Email + password authentication |
| Register | `/register/` | New user creation |
| Dashboard | `/dashboard/` | Stats overview + quick actions |
| Patients | `/patients/` | CRUD table with add/edit modals |
| Doctors | `/doctors/` | CRUD table with add/edit modals |
| Mappings | `/mappings/` | Doctor-patient assignment management |

- All API calls include the JWT token automatically via `localStorage`
- Pages are auth-guarded — redirects to login if no token found
- Dark theme with responsive design

---

## 8. How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Prateek-2812/Healthcare-Backend-Django.git
cd Healthcare-Backend-Django

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 5. Set up PostgreSQL
psql -h localhost -p 5432 -U postgres
# In psql:
#   CREATE DATABASE healthcare_db;
#   CREATE USER healthcare_user WITH PASSWORD 'healthcare_password';
#   GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;
#   \c healthcare_db
#   GRANT ALL ON SCHEMA public TO healthcare_user;
#   \q

# 6. Run migrations
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate

# 7. Seed database
python manage.py seed_data

# 8. Start server
python manage.py runserver
# Open http://127.0.0.1:8000/login/
```

### Test Credentials

| Email | Password |
|-------|----------|
| admin@healthcare.com | Admin@1234 |
| jane@healthcare.com | Jane@1234 |
| bob@healthcare.com | Bob@12345 |

---

## 9. Requirements Checklist

| Requirement | Status |
|-------------|--------|
| Django + DRF backend | ✅ |
| PostgreSQL database | ✅ |
| JWT authentication (simplejwt) | ✅ |
| `POST /api/auth/register/` | ✅ |
| `POST /api/auth/login/` | ✅ |
| `POST /api/patients/` — Add patient | ✅ |
| `GET /api/patients/` — List patients | ✅ |
| `GET /api/patients/<id>/` — Get patient | ✅ |
| `PUT /api/patients/<id>/` — Update patient | ✅ |
| `DELETE /api/patients/<id>/` — Delete patient | ✅ |
| `POST /api/doctors/` — Add doctor | ✅ |
| `GET /api/doctors/` — List doctors | ✅ |
| `GET /api/doctors/<id>/` — Get doctor | ✅ |
| `PUT /api/doctors/<id>/` — Update doctor | ✅ |
| `DELETE /api/doctors/<id>/` — Delete doctor | ✅ |
| `POST /api/mappings/` — Assign doctor to patient | ✅ |
| `GET /api/mappings/patient/<id>/` — Get patient's doctors | ✅ |
| `DELETE /api/mappings/<id>/` — Remove mapping | ✅ |
| Django ORM for database modeling | ✅ |
| Error handling and validation | ✅ |
| Environment variables for sensitive config | ✅ |

**All requirements have been implemented.** ✅
