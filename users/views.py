from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm

def registration(request):
	return render(request,'users/registration.html', {'title':'Εγγραφή'})

def register_doctor(request):
	if request.method == 'POST':
		u_form = UserRegisterForm(request.POST)
		p_form = UserProfileForm(request.POST)
		if u_form.is_valid() and p_form.is_valid():
			user = u_form.save()
			username = u_form.cleaned_data.get('username')
			profile = p_form.save(commit=False)
			profile.user = user
			profile.is_doctor = True
			profile.save()
			messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			return redirect('users:login')
	else:
		u_form = UserRegisterForm()
		p_form = UserProfileForm()
	return render(request,'users/register.html', {'title':'Εγγραφή Ιατρού','role':'doctor','u_form':u_form,'p_form':p_form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Το προφίλ σας ενημερώθηκε')
			return redirect('users:profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = UserProfileUpdateForm(instance=request.user.userprofile)

	if request.user.userprofile.is_doctor:
		role = 'doctor'
		title = 'Ενημέρωση Προφίλ Ιατρού'
	elif request.user.userprofile.is_pharmacist:
		role = 'pharmacist'
		title = 'Ενημέρωση Προφίλ Φαρμακοποιού'
	elif request.user.userprofile.is_company:
		role = 'company'
		title = 'Ενημέρωση Προφίλ Φαρμακευτικής Εταιρείας'
	else:
		role = 'admin'
		title = 'Ενημέρωση Προφίλ Χρήστη'

	context = {
		'title':title,
		'role':role,
		'u_form':u_form,
		'p_form':p_form
	}
	return render(request,'users/profile.html', context)
