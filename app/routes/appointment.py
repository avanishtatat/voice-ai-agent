from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db 
from app.schemas.appointment import AppointmentCreate, AppointmentCancel, AvailableSlotResponse, AppointmentReschedule

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor_schedule import DoctorSchedule

from app.utils.datetime_validation import validate_future_slot

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# Test route to verify that the appointments router is working
@router.get("/")
def test_route():
    return {"success": True, "message": "Appointment routes are working!"}

# Endpoint to book an appointment
@router.post("/book", status_code=201) 
def book_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):

    # 1. Validate patient 
    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found") 
    
    # 2. Validate that the appointment is in the future
    validate_future_slot(payload.date, payload.time)

    # 3. Validate doctor
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first() 
    if not doctor: 
        raise HTTPException(status_code=404, detail="Doctor not found") 
    
    # 4. Check doctor's schedule 
    slot = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == payload.doctor_id,
        DoctorSchedule.date == payload.date,
        DoctorSchedule.time == payload.time 
    ).with_for_update().first()

    if not slot: 
        raise HTTPException(status_code=404, detail="Slot does not exist for the doctor at the specified date and time")
    
    if not slot.is_available: 
        raise HTTPException(status_code=400, detail="Slot is already booked")
    
    # 5. Check if there's an existing appointment for the same doctor, date, and time that is still active
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == payload.doctor_id,
        Appointment.date == payload.date,
        Appointment.time == payload.time,
        Appointment.status == AppointmentStatus.booked
    ).first()

    if existing: 
        raise HTTPException(status_code=400, detail="Slot is already booked by another appointment")
    
    # 6. Create appointment
    new_appointment = Appointment(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        date=payload.date,
        time=payload.time,
        status=AppointmentStatus.booked
    )
    db.add(new_appointment)

    # 7. Mark slot as unavailable
    slot.is_available = False 

    try:
        db.commit()
        db.refresh(new_appointment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while booking the appointment")
    
    return {"success": True, "message": "Appointment booked successfully", "appointment_id": new_appointment.id}

# Endpoint to cancel an appointment
@router.post("/cancel", status_code=200)
def cancel_appointment(payload: AppointmentCancel, db: Session = Depends(get_db)):
    # 1. Validate appointment 
    appointment = db.query(Appointment).filter(Appointment.id == payload.appointment_id).first() 
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # 2. Check if already completed 
    if appointment.status == AppointmentStatus.completed:
        raise HTTPException(status_code=400, detail="Cannot cancel a completed appointment")
    
    # 3. Check if already cancelled 
    if appointment.status == AppointmentStatus.cancelled:
        raise HTTPException(status_code=400, detail="Appointment is already cancelled") 
    
    # 4. Update appointment status 
    appointment.status = AppointmentStatus.cancelled

    # 5. Mark slot as available again
    slot = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == appointment.doctor_id,
        DoctorSchedule.date == appointment.date,
        DoctorSchedule.time == appointment.time 
    ).first()

    if slot:
        slot.is_available = True

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while cancelling the appointment")
    
    return {"success": True, "message": "Appointment cancelled successfully", "appointment_id": appointment.id}

# Endpoint to get available slots for a doctor on a specific date
@router.get("/available-slots", response_model=list[AvailableSlotResponse])
def get_available_slots(doctor_id: int, date: date_type, db: Session = Depends(get_db)):
    # 1. Validate doctor 
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor: 
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # 2. Get available slots 
    slots = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == doctor_id,
        DoctorSchedule.date == date,
        DoctorSchedule.is_available.is_(True)
    ).all() 

    return slots

# Endpoint to reschedule an appointment
@router.post("/reschedule", status_code=200)
def reschedule_appointment(payload: AppointmentReschedule, db: Session = Depends(get_db)):
    # 1. Validate appointment 
    appointment = db.query(Appointment).filter(Appointment.id == payload.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # 2. Validate that the new appointment details are in the future
    validate_future_slot(payload.new_date, payload.new_time)

    # 3. Check if appointment is in a state that allows rescheduling (only booked appointments can be rescheduled)
    if appointment.status != AppointmentStatus.booked: 
        raise HTTPException(status_code=400, detail="Only booked appointments can be rescheduled")
    
    # 4. Rescheduling to the same doctor, date, and time is not allowed (no-op)
    if (appointment.doctor_id == payload.new_doctor_id and appointment.date == payload.new_date and appointment.time == payload.new_time):
        raise HTTPException(status_code=400, detail="New doctor, date, and time are the same as the current appointment details")
    
    # 5. Validate new doctor 
    doctor = db.query(Doctor).filter(Doctor.id == payload.new_doctor_id).first() 
    if not doctor: 
        raise HTTPException(status_code=404, detail="New doctor not found")
    
    # 6. Check new doctor's schedule 
    slot = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == payload.new_doctor_id,
        DoctorSchedule.date == payload.new_date,
        DoctorSchedule.time == payload.new_time 
    ).with_for_update().first()

    # 7. Check if slot exists and is available
    if not slot: 
        raise HTTPException(status_code=404, detail="Slot does not exist for the new doctor at the specified date and time")    
    
    if not slot.is_available: 
        raise HTTPException(status_code=400, detail="Slot is already booked for the new doctor at the specified date and time")
    
    # 8. Check if there's an existing appointment for the same doctor, date, and time that is still active (booked or rescheduled)
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == payload.new_doctor_id,
        Appointment.date == payload.new_date,
        Appointment.time == payload.new_time,
        Appointment.status == AppointmentStatus.booked
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Slot is already booked by another appointment for the new doctor at the specified date and time")
    
    # 9. Mark old slot as available again
    old_slot = db.query(DoctorSchedule).filter(
        DoctorSchedule.doctor_id == appointment.doctor_id,
        DoctorSchedule.date == appointment.date,
        DoctorSchedule.time == appointment.time 
    ).first()

    if old_slot:
        old_slot.is_available = True 
    
    # 10. Update appointment status and details
    appointment.status = AppointmentStatus.rescheduled

    # 11. Create new appointment with the same patient but new doctor, date, and time
    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=payload.new_doctor_id,
        date=payload.new_date,
        time=payload.new_time,
        status=AppointmentStatus.booked
    )
    db.add(new_appointment)

    # 12. Mark new slot as unavailable
    slot.is_available = False

    try: 
        db.commit()
        db.refresh(new_appointment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while rescheduling the appointment") 
    
    return {"success": True, "message": "Appointment rescheduled successfully", "appointment_id": new_appointment.id}