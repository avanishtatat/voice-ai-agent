from datetime import date, time, timedelta

from app.config.database import SessionLocal
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule
from app.models.appointment import Appointment

def seed_database():
    db = SessionLocal() # Obtains a database session from the SessionLocal class, allowing us to interact with the database for seeding data.
    try:
        # Prevent duplicate seeding
        if db.query(Doctor).first() or db.query(Patient).first():
            print("Data already seeded.")
        else:
        # Patients
            patient1 = Patient(name="Avanish", preferred_language="en", phone="1234567890")
            patient2 = Patient(name="Rahul", preferred_language="hi", phone="0987654321")
            patient3 = Patient(name="Arun", preferred_language="ta", phone="1122334455")

            db.add_all([patient1, patient2, patient3])

            # Doctors
            doctor1 = Doctor(name="Dr Sharma", specialty="Cardiologist")
            doctor2 = Doctor(name="Dr Meena", specialty="Dermatologist")
            doctor3 = Doctor(name="Dr Kumar", specialty="Orthopedic")

            db.add_all([doctor1, doctor2, doctor3])
            db.flush()

            # Important: IDs are generated after flush, so we can use them for schedules
            day1 = date.today() + timedelta(days=7)   # 1 week from now
            day2 = date.today() + timedelta(days=14)  # 2 weeks from now
            day3 = date.today() + timedelta(days=21)  # 3 weeks from now

            schedules = [
                # Dr Sharma – Cardiologist
                DoctorSchedule(doctor_id=doctor1.id, date=day1, time=time(9, 0)),
                DoctorSchedule(doctor_id=doctor1.id, date=day1, time=time(10, 0)),
                DoctorSchedule(doctor_id=doctor1.id, date=day1, time=time(11, 0)),
                DoctorSchedule(doctor_id=doctor1.id, date=day2, time=time(9, 0)),
                DoctorSchedule(doctor_id=doctor1.id, date=day2, time=time(10, 0)),
                # Dr Meena – Dermatologist
                DoctorSchedule(doctor_id=doctor2.id, date=day1, time=time(13, 0)),
                DoctorSchedule(doctor_id=doctor2.id, date=day1, time=time(14, 0)),
                DoctorSchedule(doctor_id=doctor2.id, date=day2, time=time(13, 0)),
                DoctorSchedule(doctor_id=doctor2.id, date=day2, time=time(15, 0)),
                # Dr Kumar – Orthopedic
                DoctorSchedule(doctor_id=doctor3.id, date=day2, time=time(11, 0)),
                DoctorSchedule(doctor_id=doctor3.id, date=day2, time=time(16, 0)),
                DoctorSchedule(doctor_id=doctor3.id, date=day3, time=time(10, 0)),
                DoctorSchedule(doctor_id=doctor3.id, date=day3, time=time(11, 0)),
            ]

            db.add_all(schedules)
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

            print("Seed data inserted successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    """Run this script to seed the database with initial data for patients, doctors, and doctor schedules."""
    seed_database()