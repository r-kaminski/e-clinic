from django.db import models, connection
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Data(models.Model):
    data_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    telephone_number = models.IntegerField()
    email = models.CharField(max_length=50)

    class Meta:
        db_table = 'data'


class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=20)
    building_number = models.IntegerField()
    city = models.CharField(max_length=50)

    class Meta:
        db_table = 'address'


class Clinic(models.Model):
    clinic_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    reception_telephone = models.IntegerField()
    email = models.CharField(max_length=50)

    class Meta:
        db_table = 'clinic'


class Doctor(models.Model):
    doctor_id = models.IntegerField(primary_key=True)
    data = models.ForeignKey(Data, models.DO_NOTHING)
    specialization = models.CharField(max_length=50)
    clinic = models.ForeignKey(Clinic, models.DO_NOTHING)
    company_telephone = models.IntegerField()

    class Meta:
        db_table = 'doctor'


class Patient(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    data = models.ForeignKey(Data, models.DO_NOTHING)

    class Meta:
        db_table = 'patient'


class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    price = models.IntegerField()
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    appointment_date = models.DateField()
    address = models.ForeignKey(Address, models.DO_NOTHING)

    class Meta:
        db_table = 'appointment'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()
