from datetime import datetime
from fastapi import HTTPException

def validate_future_slot(slot_date, slot_time):
    now = datetime.now()

    selected_datetime = datetime.combine(slot_date, slot_time)
    if selected_datetime <= now:
        raise HTTPException(status_code=400, detail="Appointment must be scheduled for a future date and time")
