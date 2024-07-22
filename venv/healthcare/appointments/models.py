from django.db import models
from django.conf import settings
from datetime import timedelta
import datetime

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE, limit_choices_to={'user_type': 1})
    doctor = models.ForeignKey(Doctor, related_name='appointments', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        start_datetime = datetime.combine(self.date, self.start_time)
        self.end_time = (start_datetime + timedelta(minutes=45)).time()
        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.get_full_name()} with {self.doctor.user.get_full_name()} on {self.date}"
