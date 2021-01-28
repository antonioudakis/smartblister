from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import PatientProfile, PharmacistProfile


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

	doctor = models.ForeignKey(User, null = True, on_delete=models.PROTECT)
	date_issued = models.DateField(default=timezone.now)
	medicine = models.CharField(max_length=255)
	quantity = models.IntegerField(choices=quantity_choices,default=1)
	dosage = models.IntegerField(choices=quantity_choices,default=1)
	frequency = models.IntegerField(choices=frequency_choices,default=1)
	duration = models.IntegerField(choices=duration_choices,default=1)

class BlisterPrescription(models.Model):
	blister = models.ForeignKey(Blister, on_delete=models.PROTECT)
	prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT)


#class Child(models.Model):
#	name = models.CharField(max_length=250)
#	parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
#	class Meta:
#		verbose_name = "Child"
#		verbose_name_plural = "Children"
#	def __str__(self):
#		return self.name