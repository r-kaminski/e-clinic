from webapp.models import Data, Address, Clinic, Doctor, Appointment
from faker import Faker
import random

fake = Faker()

if len(Appointment.objects.all()) > 0:
    print("Database already populated - skipping.")
    quit()
else:
    print("Database not populated - doing it right now.")

range_start = 10**8
range_end = 10**9

cities = []
# List of 12 specializations
specializations = ['Cardiology', 'Dermatology', 'Emergency medicine', 'Endocrinology', 'Family Medicine',
'General surgery', 'Geriatrics', 'Hermatology', 'Internal medicine', 'Neurology', 
'Pediatrics', 'Ortropedic surgery']

# Create 20 cities
for i in range(20):
    city = fake.city()
    cities.append(city)


# For each city create 5 clinics with addresses (100 clinics total)
for city in cities:
    for i in range(5):
        street = fake.street_name()
        building_number = fake.street_address().split(' ')[0]
        address = Address.objects.create(street=street, building_number=building_number, city=city)
        address.save()

        clinic_name = city + " " + street + " Hospital"
        phone_number = random.randint(range_start, range_end)
        email = fake.email()
        clinic = Clinic.objects.create(name=clinic_name, address=address, reception_telephone=phone_number, email=email)
        clinic.save()


# For each clinic, create 5 doctors (500 doctors total)
for clinic in Clinic.objects.all():
    # Take 5 random specializations
    specs = random.sample(specializations, k=5)
    for spec in specs:
        first_name = fake.first_name()
        last_name = fake.last_name()
        telephone_number = random.randint(range_start, range_end)
        email = fake.email()
        data = Data.objects.create(first_name=first_name, last_name=last_name, telephone_number=telephone_number, email=email)
        data.save()

        company_telephone = random.randint(range_start, range_end)
        doctor = Doctor.objects.create(data=data, specialization=spec, clinic=clinic, company_telephone=company_telephone)
        doctor.save()

# For each doctor, create 4 appointments (2000 appointments total)
for doctor in Doctor.objects.all():
    price = random.randint(5, 10) * 25
    for i in range(8):
        appointment_date = fake.date_this_year(before_today=False, after_today=True)
        clinic = Clinic.objects.get(clinic_id=doctor.clinic.clinic_id)
        address = clinic.address
        appointment = Appointment.objects.create(price=price, doctor=doctor, appointment_date=appointment_date, address=address)
        appointment.save()
