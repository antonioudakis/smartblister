from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import PatientProfile, PharmacistProfile
from doctor.models import Prescription


class Blister(models.Model):
	serial = models.CharField(max_length=20)
	#blister = models.ForeignKey(Blister, on_delete=models.CASCADE)
	patient = models.ForeignKey(PatientProfile, null=True, on_delete=models.PROTECT)
	pharmacist = models.ForeignKey(PharmacistProfile, null=True, on_delete=models.CASCADE)
	#serial = models.CharField(max_length=20)
	#user = models.ForeignKey(User, on_delete=models.CASCADE)
	charge_date = models.DateField(default=timezone.now)
	#desease = models.CharField(max_length=50,blank=True)
	#medicine = models.CharField(max_length=100,blank=True)
	#quantity = models.IntegerField(null=True,blank=True)
	#frequency = models.PositiveSmallIntegerField(choices=frequency_choices,default=1,blank=True)
	#active = models.BooleanField(default=False,blank=True)
	#confirmation_send = models.BooleanField(default=False,blank=True)

	def __str__(self):
		return self.patient.user.last_name+' '+self.patient.user.first_name[:1]+'. Blister [S/N '+self.serial+']'+' Charged on: '+self.charge_date.strftime('%d-%m-%Y')


class BlisterPrescription(models.Model):
	blister = models.ForeignKey(Blister, on_delete=models.PROTECT)
	prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT)

	def __str__(self):
		return self.blister.serial+' '+self.prescription.medicine+' '+str(self.prescription.date_issued)


class BlisterAction(models.Model):
	blisterPrescription = models.ForeignKey(BlisterPrescription, on_delete=models.PROTECT)
	date_removed = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.blisterPrescription.blister.serial+' '+str(self.date_removed)