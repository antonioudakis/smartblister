from rest_framework import serializers
from .models import Task
from doctor.models import Prescription
from pharmacist.models import Blister, BlisterPrescription, BlisterAction
from users.models import PatientProfile, DoctorProfile
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = '__all__'

class ChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blister
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['last_name','first_name']

class DoctorSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False)
	class Meta:
		model = DoctorProfile
		fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
	user = UserSerializer(many=False)
	doctor = DoctorSerializer(many=False)
	class Meta:
		model = PatientProfile
		fields = ['user','doctor']

class PrescriptionSerializer(serializers.ModelSerializer):
	doctor = DoctorSerializer(many=False)
	class Meta:
		model = Prescription
		fields = ['doctor','illness','medicine']

class BlisterSerializer(serializers.ModelSerializer):
	patient = PatientSerializer(many=False)
	class Meta:
		model = Blister
		fields = ['serial','charge_date','patient']

class BlisterPrescriptionSerializer(serializers.ModelSerializer):
	blister = BlisterSerializer(many=False)
	prescription = PrescriptionSerializer(many=False)
	class Meta:
		model = BlisterPrescription
		fields = ['blister','prescription']


class BlisterActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlisterAction
		fields = ['date_removed']

class RemovalSerializer(serializers.Serializer):
    date_removed__date = serializers.DateField()
    removals = serializers.IntegerField()
