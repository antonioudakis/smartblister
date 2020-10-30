from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Charge
from users.models import UserProfile
from .forms import ChildFormset, PatientSearchForm
from django.contrib import messages 

@login_required
def charge(request,user_id):
	patient = User.objects.get(pk=user_id)
	if request.method == 'POST':
		formset = ChildFormset(request.POST, instance=patient)
		if formset.is_valid():
			formset.save()
			return redirect('pharmacist:charge', user_id=patient.id)
		else:
			for value in formset.errors:
				messages.error(request, value)
			
	formset = ChildFormset(instance=patient)

	profile = UserProfile.objects.get(user=patient.id)
	context = {
		'formset':formset,
		'patient':patient.last_name+" "+patient.first_name+" (AMKA "+profile.amka+")",
	}
	return render(request,'pharmacist/parent_form.html',context)

@login_required
def charge_init(request):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			users = UserProfile.objects.filter(amka__startswith=amka)
			users = users.filter(is_patient=True)
		else:
			users = None
	else:
		form = PatientSearchForm()
		users = None


	context = {
		'title':'Χρέωση smartblister',
		'form':form,
		'users':users
	}
	
	return render(request,'pharmacist/parent_list.html', context)
