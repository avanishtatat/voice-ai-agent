from pydantic import BaseModel
from datetime import date, time

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    time: time

class AppointmentCancel(BaseModel):
    appointment_id: int

class AvailableSlotResponse(BaseModel):
    time: time

class AvailableSlotsResponse(BaseModel):
    success: bool
    available_slots: list[AvailableSlotResponse]

class AppointmentReschedule(BaseModel):
    appointment_id: int 
    new_doctor_id: int
    new_date: date
    new_time: time