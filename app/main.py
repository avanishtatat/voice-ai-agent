from fastapi import FastAPI
from app.routes.appointments import router as appointments_router
from app.routes.health import router as health_router 
from app.config.database import engine, Base 

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.doctor_schedule import DoctorSchedule

app = FastAPI(
    title="Voice AI Agent",
    description="A Voice AI Agent that can understand and respond to voice commands.",
    version="1.0.0"
) 

Base.metadata.create_all(bind=engine) # Creates the database tables based on the defined models if they don't already exist.

app.include_router(health_router)
app.include_router(appointments_router)

@app.get("/") 
def home():
    return {"message" : "Voice AI Agent is running!"}