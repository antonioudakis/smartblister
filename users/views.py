from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserUpdateForm, UserProfileForm, DoctorProfileForm, PharmacistProfileForm, PharmacyProfileForm

def registration(request):
	return render(request,'users/registration.html', {'title':'Εγγραφή'})

def register_doctor(request):
	if request.method == 'POST':
		u_form = UserRegisterForm(request.POST)
		p_form = UserProfileForm(request.POST)
		p1_form = DoctorProfileForm(request.POST)
		if u_form.is_valid() and p_form.is_valid() and p1_form.is_valid():
			user = u_form.save()
			username = u_form.cleaned_data.get('username')
			profile = p_form.save(commit=False)
			profile.user = user
			profile.is_doctor = True
			profile.save()
			doctor_profile = p1_form.save(commit=False)
			doctor_profile.user = user
			doctor_profile.save()
			messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			return redirect('login')
	else:
		u_form = UserRegisterForm()
		p_form = UserProfileForm()
		p1_form = DoctorProfileForm()

	context = {
		'title':'Εγγραφή Ιατρού',
		'role':'doctor',
		'u_form':u_form,
		'p_form':p_form,
		'p1_form':p1_form,
	}

	return render(request,'users/register.html', context)

def register_pharmacist(request):
	if request.method == 'POST':
		u_form = UserRegisterForm(request.POST)
		p_form = UserProfileForm(request.POST)
		p1_form = PharmacistProfileForm(request.POST)
		if u_form.is_valid() and p_form.is_valid() and p1_form.is_valid():
			user = u_form.save()
			username = u_form.cleaned_data.get('username')
			profile = p_form.save(commit=False)
			profile.user = user
			profile.is_pharmacist = True
			profile.save()
			pharmacist_profile = p1_form.save(commit=False)
			pharmacist_profile.user = user
			pharmacist_profile.save()
			messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			return redirect('login')
	else:
		u_form = UserRegisterForm()
		p_form = UserProfileForm()
		p1_form = PharmacistProfileForm()

	context = {
		'title':'Εγγραφή Φαρμακοποιού',
		'role':'pharmacist',
		'u_form':u_form,
		'p_form':p_form,
		'p1_form':p1_form
	}

	return render(request,'users/register.html', context)

def register_pharmacy(request):
	if request.method == 'POST':
		u_form = UserRegisterForm(request.POST)
		p_form = UserProfileForm(request.POST)
		p1_form = PharmacyProfileForm(request.POST)
		if u_form.is_valid() and p_form.is_valid() and p1_form.is_valid():
			user = u_form.save()
			username = u_form.cleaned_data.get('username')
			profile = p_form.save(commit=False)
			profile.user = user
			profile.is_pharmacy = True
			profile.save()
			pharmacy_profile = p1_form.save(commit=False)
			pharmacy_profile.user = user
			pharmacy_profile.save()
			messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			return redirect('login')
	else:
		u_form = UserRegisterForm()
		p_form = UserProfileForm()
		p1_form = PharmacyProfileForm()

	context = {
		'title':'Εγγραφή Φαρμακευτικής Εταιρείας',
		'role':'pharmacy',
		'u_form':u_form,
		'p_form':p_form,
		'p1_form':p1_form
	}

	return render(request,'users/register.html', context)

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = UserProfileForm(request.POST, instance=request.user.userprofile)
		if request.user.userprofile.is_doctor:
			p1_form = DoctorProfileForm(request.POST, instance=request.user.doctorprofile)
		elif request.user.userprofile.is_pharmacist:
			p1_form = PharmacistProfileForm(request.POST, instance=request.user.pharmacistprofile)
		elif request.user.userprofile.is_pharmacy:
			p1_form = PharmacyProfileForm(request.POST, instance=request.user.pharmacyprofile)
		else:
			pass

		if u_form.is_valid() and p_form.is_valid() and p1_form.is_valid():
			u_form.save()
			p_form.save()
			p1_form.save()
			messages.success(request, f'Το προφίλ σας ενημερώθηκε')
			return redirect('users:profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = UserProfileForm(instance=request.user.userprofile)
		if request.user.userprofile.is_doctor:
			p1_form = DoctorProfileForm(instance=request.user.doctorprofile)
		elif request.user.userprofile.is_pharmacist:
			p1_form = PharmacistProfileForm(instance=request.user.pharmacistprofile)
		elif request.user.userprofile.is_pharmacy:
			p1_form = PharmacyProfileForm(instance=request.user.pharmacyprofile)
		else:
			pass

	if request.user.userprofile.is_doctor:
		role = 'doctor'
		title = 'Ενημέρωση Προφίλ Ιατρού'
	elif request.user.userprofile.is_pharmacist:
		role = 'pharmacist'
		title = 'Ενημέρωση Προφίλ Φαρμακοποιού'
	elif request.user.userprofile.is_pharmacy:
		role = 'pharmacy'
		title = 'Ενημέρωση Προφίλ Φαρμακευτικής Εταιρείας'
	else:
		role = 'user'
		title = 'Ενημέρωση Προφίλ Χρήστη'

	context = {
		'title':title,
		'role':role,
		'u_form':u_form,
		'p_form':p_form,
		'p1_form':p1_form
	}
	return render(request,'users/profile.html', context)
