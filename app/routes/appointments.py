from fastapi import APIRouter

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.get("/")
def get_appointments():
    return {"message": "All appointments"}