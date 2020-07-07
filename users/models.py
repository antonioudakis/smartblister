from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
	id_type_choices = (
		(1,'Αστυνομική'),
		(2,'Διαβατήριο'),
		(3,'Στρατιωτική')
	)
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	birthdate = models.DateField(default=timezone.now)
	cell_phone = models.BigIntegerField(blank=True)
	id_num = models.CharField(max_length=8,unique=True,default='')
	id_type = models.PositiveSmallIntegerField(choices=id_type_choices,default=1)
	id_date_issued = models.DateField(default=timezone.now)
	id_place_issued = models.CharField(max_length=100,default='')
	father_name = models.CharField(max_length=50,blank=True)
	is_doctor = models.BooleanField(default=False)
	is_pharmacist = models.BooleanField(default=False)
	is_pharmacy = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username