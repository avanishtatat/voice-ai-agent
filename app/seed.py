from datetime import date, time, timedelta

from app.config.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.doctor_schedule import DoctorSchedule


db = next(get_db()) # Obtains a database session from the get_db generator function, allowing us to interact with the database for seeding data.

try:
    # Prevent duplicate seeding
    if db.query(Doctor).first():
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
        db.commit()

        # Important: IDs available after commit
        tomorrow = date.today() + timedelta(days=1)

        schedules = [
            DoctorSchedule(doctor_id=doctor1.id, date=tomorrow, time=time(10, 0)),
            DoctorSchedule(doctor_id=doctor1.id, date=tomorrow, time=time(11, 0)),
            DoctorSchedule(doctor_id=doctor2.id, date=tomorrow, time=time(14, 0)),
            DoctorSchedule(doctor_id=doctor2.id, date=tomorrow, time=time(15, 0)),
            DoctorSchedule(doctor_id=doctor3.id, date=tomorrow, time=time(16, 0)),
        ]

        db.add_all(schedules)
        db.commit()

        print("Seed data inserted successfully.")

finally:
    db.close()