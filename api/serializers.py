from rest_framework import serializers
from .models import Task
from pharmacist.models import Blister

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = '__all__'

class ChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blister
		fields = '__all__'