from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import UserProfile, DoctorProfile, PharmacistProfile, PharmacyProfile, PatientProfile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	last_name = forms.CharField(label='Επώνυμο')
	first_name = forms.CharField(label='Όνομα')

	class Meta:
		model = User
		fields = ['username','email','last_name','first_name','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	last_name = forms.CharField(label='Επώνυμο')
	first_name = forms.CharField(label='Όνομα')

	class Meta:
		model = User
		fields = ['username','email','last_name','first_name']

class UserProfileForm(forms.ModelForm):
	id_type_choices = (
		(1,'Αστυνομική'),
		(2,'Διαβατήριο'),
		(3,'Στρατιωτική')
	)
	amka = forms.CharField(label='ΑΜΚΑ',max_length=11)
	father_name = forms.CharField(label='Πατρώνυμο',max_length=50,required=False)
	birthdate = forms.DateField(label='Ημ/νία Γέννησης',required=False)
	cell_phone = forms.IntegerField(label='Κινητό Τηλέφωνο',required=False)
	id_num = forms.CharField(label='Αρ. Ταυτότητας',max_length=8)
	id_type = forms.ChoiceField(label='Τύπος Ταυτότητας',choices=id_type_choices)
	id_date_issued = forms.DateField(label='Ημ/νία Έκδοσης')
	id_place_issued = forms.CharField(label='Τόπος Έκδοσης',max_length=100)

	class Meta:
		model = UserProfile
		fields = ['amka','father_name','birthdate','cell_phone','id_num','id_type','id_date_issued','id_place_issued']

class DoctorProfileForm(forms.ModelForm):
	speciality = forms.CharField(label='Ειδικότητα')
	office_place = forms.CharField(label='Περιοχή Ιατρείου')

	class Meta:
		model = DoctorProfile
		fields = ['speciality','office_place']

class PharmacistProfileForm(forms.ModelForm):
	name = forms.CharField(label='Επωνυμία Φαρμακείου',required=False)
	tax_num = forms.CharField(label='ΑΦΜ Φαρμακείου')
	doy = forms.CharField(label='ΔΟΥ')
	city = forms.CharField(label='Πόλη')
	address = forms.CharField(label='Οδός')
	address_no = forms.IntegerField(label='Αριθμός')
	TK = forms.IntegerField(label='Τ.Κ.')

	class Meta:
		model = PharmacistProfile
		fields = ['name','tax_num','doy','city','address','address_no','TK']

class PharmacyProfileForm(forms.ModelForm):
	name = forms.CharField(label='Επωνυμία Φαρμακευτικής Εταιρείας',required=False)
	tax_num = forms.CharField(label='ΑΦΜ Φαρμακευτικής Εταιρείας')
	doy = forms.CharField(label='ΔΟΥ')
	city = forms.CharField(label='Πόλη')
	address = forms.CharField(label='Οδός')
	address_no = forms.IntegerField(label='Αριθμός')
	TK = forms.IntegerField(label='Τ.Κ.')

	class Meta:
		model = PharmacyProfile
		fields = ['name','tax_num','doy','city','address','address_no','TK']

class PatientProfileForm(forms.ModelForm):
	doctor = forms.ModelChoiceField(label='Επιβλέπων Ιατρός',queryset=DoctorProfile.objects.all().order_by('user__last_name'),required=False)

	class Meta:
		model = PatientProfile
		fields = ['doctor']

