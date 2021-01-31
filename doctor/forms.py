from django import forms
from django.utils import timezone
from users.models import UserProfile, PatientProfile
from .models import Prescription, Frequency, Duration


class PatientSearchForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	amka = forms.CharField(label='AMKA',initial='',help_text='Εισαγωγή ΑΜΚΑ ασθενούς')

class MonitoringRequestForm(forms.Form):
	#patient = forms.ModelChoiceField(label='Ασθενής',queryset=PatientProfile.objects.all().order_by('user__last_name'))
	user = forms.CharField(widget = forms.CharField(), required = False)


class PrescriptionAddForm(forms.ModelForm):
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

	date_issued = forms.DateField(label='Ημ/νία Έκδοσης',initial=timezone.now())
	illness = forms.CharField(label='Πάθηση',max_length=255)
	medicine = forms.CharField(label='Φάρμακο', max_length=255)
	quantity = forms.ChoiceField(label='Ποσότητα', choices=quantity_choices)
	dosage = forms.ChoiceField(label='Δοσολογία σε δισκία', choices=quantity_choices)
	frequency = forms.ModelChoiceField(label='Συχνότητα',queryset=Frequency.objects.all().order_by('id'), initial=1)
	duration = forms.ModelChoiceField(label='Διάρκεια',queryset=Duration.objects.all().order_by('id'), initial=1)
	#duration = forms.ChoiceField(label='Διάρκεια', choices=duration_choices)

	class Meta:
		model = Prescription
		fields = '__all__'
		#exclude ['patient','doctor']



