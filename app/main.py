from fastapi import FastAPI
from app.routes.appointments import router as appointments_router
from app.routes.health import router as health_router

app = FastAPI(
    title="Voice AI Agent",
    description="A Voice AI Agent that can understand and respond to voice commands.",
    version="1.0.0"
) 

app.include_router(health_router)
app.include_router(appointments_router)

@app.get("/") 
def home():
    return {"message" : "Voice AI Agent is running!"}