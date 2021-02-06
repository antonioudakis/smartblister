from django.forms.models import inlineformset_factory
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from users.models import PatientProfile
from .models import Blister,BlisterPrescription
from doctor.models import Prescription
#from django.contrib.admin.widgets import AdminDateWidget
#from django.forms.fields import DateField

ChildFormset = inlineformset_factory(
	PatientProfile, Blister, fields=('serial','patient','charge_date'),extra=1,
)

class PatientSearchForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	amka = forms.CharField(label='AMKA',help_text='Εισαγωγή ΑΜΚΑ ασθενούς')

class BlisterAddForm(forms.ModelForm):
	serial = forms.CharField(label="Σειριακός Αριθμός")
	#charge_date = forms.DateField(label="Ημ/νία Χρέωσης",widget=forms.HiddenInput())
	#charge_date = forms.DateField(label="Ημ/νία Χρέωσης",initial=timezone.now,widget=AdminDateWidget)
	charge_date = forms.DateField(label="Ημ/νία Χρέωσης",initial=timezone.now)

	class Meta:
		model = Blister
		fields = ['serial','charge_date']


class BlisterPrescriptionForm(forms.ModelForm):

	#prescription = forms.ModelChoiceField(label='Συνταγή',queryset=Prescription.objects.none())

	#prescription = forms.ModelChoiceField(label='Συνταγή',queryset=Prescription.objects.filter(patient__id=patient_id).order_by('-date_issued'))

	def __init__(self, *args, **kwargs):
		patient_id = kwargs.pop('patient_id')
		super(BlisterPrescriptionForm, self).__init__(*args, **kwargs)
		self.fields['prescription'] = forms.ModelChoiceField(label='Συνταγή',queryset=Prescription.objects.filter(patient__id=patient_id).order_by('-date_issued'))

	class Meta:
		model = BlisterPrescription
		fields = ['prescription']





