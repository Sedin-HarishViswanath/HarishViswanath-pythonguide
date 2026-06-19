class Person:
    def __init__(self, name: str, age: int, contact: str):
        self.__name = name
        self.__age = age
        self.__contact = contact

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def contact(self):
        return self.__contact

# ---------------- Doctor ----------------

class Doctor(Person):
    def __init__(
        self,
        doctor_id: int,
        name: str,
        age: int,
        contact: str,
        specialization: str,
        fee: float
    ):
        super().__init__(name, age, contact)

        self.__doctor_id = doctor_id
        self.__specialization = specialization
        self.__fee = fee

    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def specialization(self):
        return self.__specialization

    @property
    def fee(self):
        return self.__fee

    def __str__(self):
        return (
            f"Doctor ID: {self.__doctor_id}, "
            f"Dr. {self.name} ({self.__specialization}) "
            f"Fee: ₹{self.__fee}"
        )


# ---------------- Patient ----------------

class Patient(Person):
    def __init__(
        self,
        patient_id: int,
        name: str,
        age: int,
        contact: str
    ):
        super().__init__(name, age, contact)

        self.__patient_id = patient_id
        self.__appointments = []

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def appointment_count(self):
        return len(self.__appointments)

    def book_appointment(self, doctor):
        self.__appointments.append(doctor)

    def get_appointments(self):
        return self.__appointments.copy()

    def __str__(self):
        return f"Patient ID: {self.__patient_id}, {self.name}"


# ---------------- Hospital ----------------

class Hospital:
    def __init__(self, name: str):
        self.name = name
        self.__doctors = []
        self.__patients = []

    def add_doctor(self, doctor: Doctor):
        self.__doctors.append(doctor)

    def add_patient(self, patient: Patient):
        self.__patients.append(patient)

    def find_doctor(self, specialization: str):
        return [
            doctor
            for doctor in self.__doctors
            if doctor.specialization.lower() ==
               specialization.lower()
        ]

    def book_appointment(
        self,
        patient: Patient,
        doctor: Doctor
    ):
        patient.book_appointment(doctor)

        print(
            f"Appointment booked for "
            f"{patient.name} with Dr. {doctor.name}"
        )

    def daily_summary(self):
        print("\n===== DAILY SUMMARY =====")
        print(f"Doctors  : {len(self.__doctors)}")
        print(f"Patients : {len(self.__patients)}")

        total_appointments = sum(
            patient.appointment_count
            for patient in self.__patients
        )

        print(f"Appointments : {total_appointments}")

    # Bonus
    def billing_report(self, patient: Patient):
        print("\n===== BILLING REPORT =====")
        print(f"Patient : {patient.name}")

        total = 0

        for doctor in patient.get_appointments():
            print(
                f"Dr. {doctor.name:<15} "
                f"₹{doctor.fee}"
            )
            total += doctor.fee

        print("-" * 30)
        print(f"Total Bill : ₹{total}")

# ---------------- TESTING ----------------

hospital = Hospital("Apollo Hospital")

# Doctors
d1 = Doctor(
    1,
    "Ramesh",
    45,
    "9876543210",
    "Cardiology",
    1000
)

d2 = Doctor(
    2,
    "Priya",
    38,
    "9876543222",
    "Dermatology",
    800
)

hospital.add_doctor(d1)
hospital.add_doctor(d2)

# Patients
p1 = Patient(
    101,
    "Harish",
    21,
    "9999999999"
)

hospital.add_patient(p1)

# Search Doctor
print("Cardiology Doctors:")
for doctor in hospital.find_doctor("Cardiology"):
    print(doctor)

# Book appointments
hospital.book_appointment(p1, d1)
hospital.book_appointment(p1, d2)

# Summary
hospital.daily_summary()

# Invoice
hospital.billing_report(p1)