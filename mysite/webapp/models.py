# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    appointment_date = models.DateField()
    address = models.ForeignKey(Address, models.DO_NOTHING)

    class Meta:
        db_table = 'appointment'



#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()


#class Insertion():
#
#    def insert_clinic(self, street, building_number, city, name, reception_telephone, email):
#        cursor = connection.cursor()
#        cursor.callproc('insert_clinic', [street, building_number, city, name, reception_telephone, email,])
#        cursor.close()
