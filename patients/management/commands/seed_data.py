"""
Management command to seed the database with synthetic healthcare data.
Inserts users, patients, doctors, and patient-doctor mappings directly
through Django ORM (actual database entries, not via API).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


class Command(BaseCommand):
    help = 'Seed database with synthetic healthcare data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database with synthetic data...'))

        # ── 1. Create Users ──────────────────────────────────────────────
        users_data = [
            {'username': 'dr_admin', 'email': 'admin@healthcare.com', 'password': 'Admin@1234'},
            {'username': 'nurse_jane', 'email': 'jane@healthcare.com', 'password': 'Jane@1234'},
            {'username': 'receptionist_bob', 'email': 'bob@healthcare.com', 'password': 'Bob@12345'},
        ]

        users = []
        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={'email': u['email']}
            )
            if created:
                user.set_password(u['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  Created user: {user.username}'))
            else:
                self.stdout.write(f'  User already exists: {user.username}')
            users.append(user)

        admin_user, nurse_user, receptionist_user = users

        # ── 2. Create Doctors ────────────────────────────────────────────
        doctors_data = [
            {
                'name': 'Rajesh Kumar',
                'specialization': 'Cardiology',
                'phone': '+91-9876543210',
                'email': 'rajesh.kumar@hospital.com',
                'experience_years': 15,
                'created_by': admin_user,
            },
            {
                'name': 'Priya Sharma',
                'specialization': 'Dermatology',
                'phone': '+91-9876543211',
                'email': 'priya.sharma@hospital.com',
                'experience_years': 10,
                'created_by': admin_user,
            },
            {
                'name': 'Amit Patel',
                'specialization': 'Orthopedics',
                'phone': '+91-9876543212',
                'email': 'amit.patel@hospital.com',
                'experience_years': 20,
                'created_by': nurse_user,
            },
            {
                'name': 'Sneha Reddy',
                'specialization': 'Pediatrics',
                'phone': '+91-9876543213',
                'email': 'sneha.reddy@hospital.com',
                'experience_years': 8,
                'created_by': nurse_user,
            },
            {
                'name': 'Vikram Singh',
                'specialization': 'Neurology',
                'phone': '+91-9876543214',
                'email': 'vikram.singh@hospital.com',
                'experience_years': 12,
                'created_by': admin_user,
            },
            {
                'name': 'Ananya Gupta',
                'specialization': 'Ophthalmology',
                'phone': '+91-9876543215',
                'email': 'ananya.gupta@hospital.com',
                'experience_years': 6,
                'created_by': receptionist_user,
            },
            {
                'name': 'Suresh Menon',
                'specialization': 'General Medicine',
                'phone': '+91-9876543216',
                'email': 'suresh.menon@hospital.com',
                'experience_years': 25,
                'created_by': admin_user,
            },
            {
                'name': 'Kavita Joshi',
                'specialization': 'Gynecology',
                'phone': '+91-9876543217',
                'email': 'kavita.joshi@hospital.com',
                'experience_years': 14,
                'created_by': nurse_user,
            },
        ]

        doctors = []
        for d in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=d['name'],
                defaults={
                    'specialization': d['specialization'],
                    'phone': d['phone'],
                    'email': d['email'],
                    'experience_years': d['experience_years'],
                    'created_by': d['created_by'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created doctor: Dr. {doctor.name} ({doctor.specialization})'))
            else:
                self.stdout.write(f'  Doctor already exists: Dr. {doctor.name}')
            doctors.append(doctor)

        # ── 3. Create Patients ───────────────────────────────────────────
        patients_data = [
            {
                'name': 'Arjun Verma',
                'age': 45,
                'gender': 'Male',
                'phone': '+91-9000000001',
                'address': '12, MG Road, Bangalore, Karnataka',
                'medical_history': 'Hypertension, Type 2 Diabetes. On Metformin 500mg and Amlodipine 5mg.',
                'created_by': admin_user,
            },
            {
                'name': 'Meera Nair',
                'age': 32,
                'gender': 'Female',
                'phone': '+91-9000000002',
                'address': '45, Marine Drive, Mumbai, Maharashtra',
                'medical_history': 'Asthma since childhood. Uses salbutamol inhaler as needed.',
                'created_by': admin_user,
            },
            {
                'name': 'Ravi Shankar',
                'age': 58,
                'gender': 'Male',
                'phone': '+91-9000000003',
                'address': '78, Anna Salai, Chennai, Tamil Nadu',
                'medical_history': 'Coronary artery disease. Had angioplasty in 2022. On aspirin and statins.',
                'created_by': admin_user,
            },
            {
                'name': 'Lakshmi Devi',
                'age': 67,
                'gender': 'Female',
                'phone': '+91-9000000004',
                'address': '23, Jubilee Hills, Hyderabad, Telangana',
                'medical_history': 'Osteoarthritis in both knees. Cataract surgery done in 2023.',
                'created_by': nurse_user,
            },
            {
                'name': 'Sanjay Mishra',
                'age': 29,
                'gender': 'Male',
                'phone': '+91-9000000005',
                'address': '56, Connaught Place, New Delhi',
                'medical_history': 'No significant past history. Seasonal allergies.',
                'created_by': nurse_user,
            },
            {
                'name': 'Deepa Iyer',
                'age': 41,
                'gender': 'Female',
                'phone': '+91-9000000006',
                'address': '89, Koregaon Park, Pune, Maharashtra',
                'medical_history': 'Migraine disorder. On Sumatriptan as needed. Family history of hypertension.',
                'created_by': admin_user,
            },
            {
                'name': 'Karthik Subramanian',
                'age': 53,
                'gender': 'Male',
                'phone': '+91-9000000007',
                'address': '34, Race Course Road, Coimbatore, Tamil Nadu',
                'medical_history': 'Type 1 Diabetes since age 15. On insulin pump therapy.',
                'created_by': receptionist_user,
            },
            {
                'name': 'Fatima Begum',
                'age': 36,
                'gender': 'Female',
                'phone': '+91-9000000008',
                'address': '67, Hazratganj, Lucknow, Uttar Pradesh',
                'medical_history': 'Hypothyroidism. On Levothyroxine 50mcg daily.',
                'created_by': receptionist_user,
            },
            {
                'name': 'Rohan Desai',
                'age': 22,
                'gender': 'Male',
                'phone': '+91-9000000009',
                'address': '12, FC Road, Pune, Maharashtra',
                'medical_history': 'Sports injury - ACL tear in right knee (2024). Post-surgery rehab ongoing.',
                'created_by': nurse_user,
            },
            {
                'name': 'Anita Kulkarni',
                'age': 48,
                'gender': 'Female',
                'phone': '+91-9000000010',
                'address': '90, Banjara Hills, Hyderabad, Telangana',
                'medical_history': 'PCOS, iron deficiency anemia. On oral iron supplements.',
                'created_by': admin_user,
            },
        ]

        patients = []
        for p in patients_data:
            patient, created = Patient.objects.get_or_create(
                name=p['name'],
                created_by=p['created_by'],
                defaults={
                    'age': p['age'],
                    'gender': p['gender'],
                    'phone': p['phone'],
                    'address': p['address'],
                    'medical_history': p['medical_history'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Created patient: {patient.name} (Age {patient.age})'))
            else:
                self.stdout.write(f'  Patient already exists: {patient.name}')
            patients.append(patient)

        # ── 4. Create Patient-Doctor Mappings ────────────────────────────
        mappings_data = [
            (patients[0], doctors[0]),   # Arjun -> Dr. Rajesh (Cardiology)
            (patients[0], doctors[6]),   # Arjun -> Dr. Suresh (General Medicine)
            (patients[1], doctors[6]),   # Meera -> Dr. Suresh (General Medicine)
            (patients[2], doctors[0]),   # Ravi -> Dr. Rajesh (Cardiology)
            (patients[3], doctors[2]),   # Lakshmi -> Dr. Amit (Orthopedics)
            (patients[3], doctors[5]),   # Lakshmi -> Dr. Ananya (Ophthalmology)
            (patients[4], doctors[1]),   # Sanjay -> Dr. Priya (Dermatology)
            (patients[5], doctors[4]),   # Deepa -> Dr. Vikram (Neurology)
            (patients[6], doctors[6]),   # Karthik -> Dr. Suresh (General Medicine)
            (patients[6], doctors[0]),   # Karthik -> Dr. Rajesh (Cardiology)
            (patients[7], doctors[6]),   # Fatima -> Dr. Suresh (General Medicine)
            (patients[8], doctors[2]),   # Rohan -> Dr. Amit (Orthopedics)
            (patients[9], doctors[7]),   # Anita -> Dr. Kavita (Gynecology)
            (patients[4], doctors[3]),   # Sanjay -> Dr. Sneha (Pediatrics)
        ]

        for patient, doctor in mappings_data:
            mapping, created = PatientDoctorMapping.objects.get_or_create(
                patient=patient,
                doctor=doctor,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'  Mapped: {patient.name} -> Dr. {doctor.name} ({doctor.specialization})'
                ))
            else:
                self.stdout.write(f'  Mapping already exists: {patient.name} -> Dr. {doctor.name}')

        # ── Summary ──────────────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('DATABASE SEEDING COMPLETE'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  Users    : {User.objects.count()}')
        self.stdout.write(f'  Doctors  : {Doctor.objects.count()}')
        self.stdout.write(f'  Patients : {Patient.objects.count()}')
        self.stdout.write(f'  Mappings : {PatientDoctorMapping.objects.count()}')
        self.stdout.write('')
        self.stdout.write(self.style.NOTICE('Login credentials:'))
        for u in users_data:
            self.stdout.write(f'  {u["username"]} / {u["password"]}  ({u["email"]})')
        self.stdout.write('')
