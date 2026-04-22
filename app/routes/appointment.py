from datetime import date as date_type

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db 
from app.schemas.appointment import AppointmentCreate, AppointmentCancel, AvailableSlotsResponse, AppointmentReschedule

from app.services.appointment_service import book_appointment_service, cancel_appointment_service, get_available_slots_service, reschedule_appointment_service

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Test route to verify that the appointments router is working
@router.get("/")
def test_route():
    return {"success": True, "message": "Appointment routes are working!"}

# Endpoint to book an appointment
@router.post("/book", status_code=201) 
def book_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = book_appointment_service(payload, db)
    return {"success": True, "message": "Appointment booked successfully", "appointment_id": new_appointment.id}

# Endpoint to cancel an appointment
@router.post("/cancel", status_code=200)
def cancel_appointment(payload: AppointmentCancel, db: Session = Depends(get_db)):
    appointment = cancel_appointment_service(payload, db)
    return {"success": True, "message": "Appointment cancelled successfully", "appointment_id": appointment.id}

# Endpoint to get available slots for a doctor on a specific date
@router.get("/available-slots", response_model=AvailableSlotsResponse)
def get_available_slots(doctor_id: int, date: date_type, db: Session = Depends(get_db)):
    slots = get_available_slots_service(doctor_id, date, db)
    return {"success": True, "available_slots": slots}

# Endpoint to reschedule an appointment
@router.post("/reschedule", status_code=200)
def reschedule_appointment(payload: AppointmentReschedule, db: Session = Depends(get_db)):
    new_appointment = reschedule_appointment_service(payload, db)
    return {"success": True, "message": "Appointment rescheduled successfully", "appointment_id": new_appointment.id}