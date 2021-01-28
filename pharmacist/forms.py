from django.forms.models import inlineformset_factory
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from users.models import PatientProfile
from .models import Blister, Prescription
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

class Prescription(forms.ModelForm):
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

	date_issued = forms.DateField(label='Ημ/νία Έκδοσης')
	medicine = forms.CharField(label='Φάρμακο', max_length=255)
	quantity = forms.ChoiceField(label='Ποσότητα', choices=quantity_choices)
	dosage = forms.ChoiceField(label='Δοσολογία', choices=quantity_choices)
	frequency = forms.ChoiceField(label='Συχνότητα', choices=frequency_choices)
	duration = forms.ChoiceField(label='Διάρκεια', choices=duration_choices)

	class Meta:
		model = Prescription
		fields = '__all__'



