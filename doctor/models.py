from django.db import models
from users.models import PatientProfile, DoctorProfile
from django.utils import timezone
from django.contrib.auth.models import User

class MonitoringRequest(models.Model):
	doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, blank=True, null=True)
	patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, blank=True, null=True)
	date_requested = models.DateField(default=timezone.now)
	token = models.CharField(max_length=100)
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return self.doctor.user.last_name + ' ' + self.doctor.user.first_name[:1] + '. -> ' + self.patient.user.last_name + ' ' + self.patient.user.first_name[:1]
