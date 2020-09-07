from django import forms
from users.models import UserProfile, PatientProfile


class PatientSearchForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	amka = forms.CharField(label='AMKA',initial='',help_text='Εισαγωγή ΑΜΚΑ ασθενούς')

class MonitoringRequestForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	user = forms.CharField(widget = forms.CharField(), required = False)



