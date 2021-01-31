from django.db import models
from users.models import PatientProfile, DoctorProfile
from django.utils import timezone
from django.contrib.auth.models import User

class MonitoringRequest(models.Model):
	doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, blank=True, null=True)
	patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, blank=True, null=True)
	date_requested = models.DateField(default=timezone.now)
	token = models.CharField(max_length=100)
	date_accepted = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.doctor.user.last_name + ' ' + self.doctor.user.first_name[:1] + '. -> ' + self.patient.user.last_name + ' ' + self.patient.user.first_name[:1]

class Frequency(models.Model):
	description = models.CharField(max_length=50)

	def __str__(self):
		return self.description

class Duration(models.Model):
	description = models.CharField(max_length=50)

	def __str__(self):
		return self.description


class Prescription(models.Model):
	quantity_choices = (
		(1,'1'),
		(2,'2'),
		(3,'3')
	)

	frequency_choices = (
		(1,'1 φορά την ημέρα'),
		(2,'2 φορές την ημέρα'),
		(3,'3 φορές την ημέρα'),
		(4,'4 φορές την ημέρα'),
		(5,'1 φορά την εβδομάδα'),
		(6,'2 φορές την εβδομάδα'),
		(7,'3 φορές την εβδομάδα')
	)

	duration_choices = (
		(1,'για 7 ημέρες'),
		(2,'για 10 ημέρες'),
		(3,'για 2 εβδομάδες'),
		(4,'για 1 μήνα'),
		(5,'για 2 μήνες'),
		(6,'για 3 μήνες'),
		(7,'για 6 μήνες'),
		(8,'για ένα έτος')
	)

	patient = models.ForeignKey(PatientProfile, null = True, blank=True, on_delete=models.PROTECT)
	doctor = models.ForeignKey(DoctorProfile, null = True, blank=True, on_delete=models.PROTECT)
	date_issued = models.DateField(default=timezone.now)
	illness = models.CharField(max_length=255)
	medicine = models.CharField(max_length=255)
	quantity = models.IntegerField(choices=quantity_choices,default=1)
	dosage = models.IntegerField(choices=quantity_choices,default=1)
	frequency = models.ForeignKey(Frequency, on_delete=models.PROTECT, default=1)
	duration = models.ForeignKey(Duration, on_delete=models.PROTECT, default=1)
	#duration = models.IntegerField(choices=duration_choices,default=1)

	def __str__(self):
		return self.medicine+' '+str(self.date_issued)