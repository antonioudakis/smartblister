from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Charge(models.Model):
	frequency_choices = (
		(1,'1 ανά ημέρα'),
		(2,'2 ανά ημέρα'),
		(3,'3 ανά ημέρα')
	)
	serial = models.CharField(max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	charge_date = models.DateField()
	desease = models.CharField(max_length=50,blank=True)
	medicine = models.CharField(max_length=100,blank=True)
	quantity = models.IntegerField(null=True,blank=True)
	frequency = models.PositiveSmallIntegerField(choices=frequency_choices,default=1,blank=True)
	active = models.BooleanField(default=False,blank=True)
	confirmation_send = models.BooleanField(default=False,blank=True)

	def __str__(self):
		return self.serial

#class Child(models.Model):
#	name = models.CharField(max_length=250)
#	parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
#	class Meta:
#		verbose_name = "Child"
#		verbose_name_plural = "Children"
#	def __str__(self):
#		return self.name