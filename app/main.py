from fastapi import FastAPI
from contextlib import asyncccontextmanager
from app.routes.appointments import router as appointments_router
from app.routes.health import router as health_router 
from app.config.database import engine, Base 

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.doctor_schedule import DoctorSchedule

@asyncccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here (e.g., database connection, loading models)
    print("Starting up the Voice AI Agent...")
    Base.metadata.create_all(bind=engine) # Ensures that the database tables are created at startup.
    yield
    # Perform any shutdown tasks here (e.g., closing database connections)
    print("Shutting down the Voice AI Agent...")

app = FastAPI(
    title="Voice AI Agent",
    description="A Voice AI Agent that can understand and respond to voice commands.",
    version="1.0.0", 
    lifespan=lifespan
) 

app.include_router(health_router)
app.include_router(appointments_router)

@app.get("/") 
def home():
    return {"message" : "Voice AI Agent is running!"}