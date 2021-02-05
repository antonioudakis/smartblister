from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Blister,BlisterPrescription
from users.models import UserProfile,PatientProfile
from .forms import ChildFormset, PatientSearchForm, BlisterAddForm, BlisterPrescriptionForm
from django.contrib import messages 

@login_required
def chargeBlister(request,user_id):
	patient = User.objects.get(pk=user_id)
	if request.method == 'POST':
		formset = ChildFormset(request.POST, instance=patient)
		if formset.is_valid():
			formset.save()
			return redirect('pharmacist:chargeBlister', user_id=patient.id)
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
def blister(request):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		form1 = BlisterAddForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			try:
				patient = PatientProfile.objects.get(user__userprofile__amka=amka)
				blisters = patient.blister_set.all().order_by('-charge_date')
			except PatientProfile.DoesNotExist:
				patient = None
				blisters = None
		else:
			patient = None
			blisters = None
	else:
		form = PatientSearchForm()
		form1 = BlisterAddForm()
		patient = None
		blisters = None


	context = {
		'title':'Χρέωση smartblister',
		'form':form,
		'form1':form1,
		'patient':patient,
		'blisters': blisters
	}
	
	return render(request,'pharmacist/blister_list.html', context)

@login_required
def chargedBlisters(request,patient_id):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		form1 = BlisterAddForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			try:
				patient = PatientProfile.objects.get(user__userprofile__amka=amka)
				blisters = patient.blister_set.all().order_by('-charge_date')
			except PatientProfile.DoesNotExist:
				patient = None
				blisters = None
		else:
			patient = None
			blisters = None
	else:
		form = PatientSearchForm()
		form1 = BlisterAddForm()
		try:
			patient = PatientProfile.objects.get(id=patient_id)
			blisters = patient.blister_set.all().order_by('-charge_date')
		except PatientProfile.DoesNotExist:
			patient = None
			blisters = None


	context = {
		'title':'Χρέωση smartblister',
		'form':form,
		'form1':form1,
		'patient':patient,
		'blisters': blisters
	}
	
	return render(request,'pharmacist/blister_list.html', context)

@login_required
def deleteBlister(request,blister_id):
	try:
		blister = Blister.objects.get(id=blister_id)
		patient = blister.patient
		blister.delete()
		return redirect('pharmacist:chargedBlisters', patient_id=patient.id)
	except Blister.DoesNotExist:
		messages.warning(request,f'Δεν υπάρχει blister με τα στοιχεία που δώσατε')
		return redirect('pharmacist:blister')

@login_required
def addBlister(request,patient_id):
	if request.method == 'POST':
		form = BlisterAddForm(request.POST)
		patient = PatientProfile.objects.get(id=patient_id)
		if form.is_valid():
			blister = form.save(commit=False)
			blister.patient = patient
			blister.pharmacist = request.user.pharmacistprofile
			blister.save()
			blisters = patient.blister_set.all().order_by('-charge_date')
			#messages.success(request,f'To blister αποθηκεύτηκε')

	else:
		form = BlisterAddForm()
		patient = PatientProfile.objects.get(id=patient_id)
		blisters = patient.blister_set.all()


	context = {
		'title':'Χρέωση smartblister',
		'form':form,
		'patient':patient,
		'blisters': blisters
	}
	
	return redirect('pharmacist:chargedBlisters', patient_id=patient.id)

@login_required
def blisterPrescription(request,patient_id,blister_id):
	blister = Blister.objects.get(id=blister_id)
	if request.method == 'POST':
		try:
			bp = BlisterPrescription.objects.get(blister=blister)
			form = BlisterPrescriptionForm(request.POST,instance=bp)
		except BlisterPrescription.DoesNotExist:
			form = BlisterPrescriptionForm(request.POST)
		if form.is_valid():
			blisterPrescription = form.save(commit=False)
			blisterPrescription.blister = blister
			patient = PatientProfile.objects.get(id=patient_id)
			blisterPrescription.save()
			#messages.success(request,f'To blister αποθηκεύτηκε')
			return redirect('pharmacist:chargedBlisters', patient_id=patient.id)
		else:
			print("not valid form")
			print(form.errors)

	else:
		patient = PatientProfile.objects.get(id=patient_id)
		try:
			bp = BlisterPrescription.objects.get(blister=blister)
			form = BlisterPrescriptionForm(instance=bp)
		except BlisterPrescription.DoesNotExist:
			form = BlisterPrescriptionForm()


	context = {
		'title':'Σύνδεση blister με συνταγή',
		'form':form,
		'patient':patient,
		'blister': blister
	}
	
	return render(request,'pharmacist/blister_prescription.html', context)

	

@login_required
def chargeBlister_init(request):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			try:
				patient = PatientProfile.objects.get(user__userprofile__amka=amka)
				blisters = patient.blister_set.all()
			except PatientProfile.DoesNotExist:
			#users = users.filter(is_patient=True)
				patient = None
				blisters = None
		else:
			patient = None
			blisters = None
	else:
		form = PatientSearchForm()
		patient = None
		blisters = None


	context = {
		'title':'Χρέωση smartblister',
		'form':form,
		'patient':patient,
		'blisters': blisters
	}
	
	return render(request,'pharmacist/parent_list.html', context)
