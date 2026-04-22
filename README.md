# Voice AI Agent – Doctor Appointment Booking System

An AI-powered backend system that enables patients to book, cancel, reschedule, and manage doctor appointments through a clean REST API — built as the foundation for a full voice-driven healthcare assistant.

---

## Project Overview

**Voice AI Agent** is a production-ready FastAPI backend that allows patients to:

- Book appointments with doctors
- Cancel existing appointments
- Reschedule appointments to a new doctor, date, and time
- View available time slots for any doctor on a given date

The backend is built using:

- **FastAPI** – high-performance async web framework
- **SQLAlchemy ORM** – database modeling and query management
- **PostgreSQL (Neon DB)** – cloud-hosted relational database
- **Pydantic v2** – strict request/response validation
- **Docker** – containerized for consistent deployments

---

## Features Implemented

- Appointment booking with full validation
- Prevent double booking on the same doctor slot
- Cancel appointment with slot restoration
- Reschedule appointment (cancel old + book new)
- Available slots API filtered by doctor and date
- Future date/time validation (no past appointments)
- Clean modular architecture: `routes / services / models / schemas`
- Database seeding script for demo data

---

## Upcoming Features (Near Future Enhancements)

- Voice assistant integration
- Speech-to-text booking commands
- Text-to-speech responses
- Basic frontend UI for patients
- JWT Authentication & role-based access
- Appointment notifications and reminders
- Admin dashboard for doctors and schedules

---

## Project Structure

```
voice-ai-agent/
├── app/
│   ├── main.py                     # FastAPI app entry point
│   ├── seed.py                     # Database seeding script
│   ├── config/
│   │   └── database.py             # DB engine, session, and Base setup
│   ├── models/
│   │   ├── appointment.py          # Appointment model & status enum
│   │   ├── doctor.py               # Doctor model
│   │   ├── doctor_schedule.py      # Doctor schedule/slot model
│   │   └── patient.py              # Patient model
│   ├── routes/
│   │   ├── appointment.py          # Appointment API routes
│   │   └── health.py               # Health check route
│   ├── schemas/
│   │   └── appointment.py          # Pydantic request/response schemas
│   ├── services/
│   │   └── appointment_service.py  # Business logic layer
│   └── utils/
│       └── datetime_validation.py  # Future date/time validation
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/appointments/book` | Book an appointment |
| POST | `/appointments/cancel` | Cancel an appointment |
| POST | `/appointments/reschedule` | Reschedule an appointment |
| GET | `/appointments/available-slots` | Get available slots for a doctor on a date |

### Request & Response Examples

#### Book an Appointment

**POST** `/appointments/book`

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "date": "2026-05-01",
  "time": "10:00:00"
}
```

**Response** `201`
```json
{
  "success": true,
  "message": "Appointment booked successfully",
  "appointment_id": 1
}
```

#### Cancel an Appointment

**POST** `/appointments/cancel`

```json
{
  "appointment_id": 1
}
```

**Response** `200`
```json
{
  "success": true,
  "message": "Appointment cancelled successfully",
  "appointment_id": 1
}
```

#### Reschedule an Appointment

**POST** `/appointments/reschedule`

```json
{
  "appointment_id": 1,
  "new_doctor_id": 2,
  "new_date": "2026-05-05",
  "new_time": "14:00:00"
}
```

**Response** `200`
```json
{
  "success": true,
  "message": "Appointment rescheduled successfully",
  "appointment_id": 2
}
```

#### Get Available Slots

**GET** `/appointments/available-slots?doctor_id=1&date=2026-05-01`

**Response** `200`
```json
[
  { "time": "10:00:00" },
  { "time": "11:00:00" }
]
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd voice-ai-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://user:password@host/dbname
```

### 5. Seed the database (optional)

```bash
python -m app.seed
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

---

## Docker Setup

### Build the image

```bash
docker build -t voice-ai-agent .
```

### Run the container

```bash
docker run -p 8000:8000 --env-file .env voice-ai-agent
```

API available at: `http://localhost:8000`

---

## Swagger Docs

| Interface | URL |
|-----------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
