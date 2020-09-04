from django import forms
from users.models import UserProfile, PatientProfile


class MonitoringRequestForm(forms.Form):
	patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))



