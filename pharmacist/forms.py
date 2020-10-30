from django.forms.models import inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import Charge

ChildFormset = inlineformset_factory(
	User, Charge, fields=('serial','charge_date','desease','medicine','quantity','frequency'),extra=1,
)

class PatientSearchForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	amka = forms.CharField(label='AMKA',initial='',help_text='Εισαγωγή ΑΜΚΑ ασθενούς')