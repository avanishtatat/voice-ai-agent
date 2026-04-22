# Voice AI Agent

A RESTful API backend for a Voice AI Agent that manages doctor appointments. Built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Features

- Book appointments with doctors
- Cancel existing appointments
- Reschedule appointments to a new doctor, date, and time
- Check available slots for a doctor on a specific date
- Automatic slot availability management
- Database seeding with sample doctors, patients, and schedules

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL (via psycopg) |
| Validation | Pydantic v2 |
| Server | Uvicorn |

## Project Structure

```
voice-ai-agent/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── seed.py                  # Database seeding script
│   ├── config/
│   │   └── database.py          # DB engine, session, and Base setup
│   ├── models/
│   │   ├── appointment.py       # Appointment model & status enum
│   │   ├── doctor.py            # Doctor model
│   │   ├── doctor_schedule.py   # Doctor schedule/slot model
│   │   └── patient.py           # Patient model
│   ├── routes/
│   │   ├── appointment.py       # Appointment API routes
│   │   └── health.py            # Health check route
│   ├── schemas/
│   │   └── appointment.py       # Pydantic request/response schemas
│   ├── services/
│   │   └── appointment_service.py  # Business logic
│   └── utils/
│       └── datetime_validation.py  # Future date/time validation
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- PostgreSQL database

## Setup

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
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/your_database
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 6. Seed the database (optional)

To populate the database with sample doctors, patients, and schedules:

```python
from app.seed import seed_database
seed_database()
```

Or add a call to `seed_database()` in your startup logic.

## API Endpoints

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/appointments/` | Test route |
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
  "doctor_id": 2,
  "date": "2026-04-23",
  "time": "14:00:00"
}
```

**Response** `201`
```json
{
  "success": true,
  "message": "Appointment booked successfully",
  "appointment_id": 5
}
```

#### Cancel an Appointment

**POST** `/appointments/cancel`

```json
{
  "appointment_id": 5
}
```

**Response** `200`
```json
{
  "success": true,
  "message": "Appointment cancelled successfully",
  "appointment_id": 5
}
```

#### Reschedule an Appointment

**POST** `/appointments/reschedule`

```json
{
  "appointment_id": 5,
  "new_doctor_id": 3,
  "new_date": "2026-04-24",
  "new_time": "16:00:00"
}
```

**Response** `200`
```json
{
  "success": true,
  "message": "Appointment rescheduled successfully",
  "appointment_id": 6
}
```

#### Get Available Slots

**GET** `/appointments/available-slots?doctor_id=1&date=2026-04-23`

**Response** `200`
```json
[
  { "time": "10:00:00" },
  { "time": "11:00:00" }
]
```

## Data Models

### Appointment Status

| Status | Description |
|--------|-------------|
| `booked` | Appointment is active |
| `cancelled` | Appointment was cancelled |
| `completed` | Appointment has been completed |
| `rescheduled` | Appointment was rescheduled |

## Interactive API Docs

FastAPI provides built-in interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
