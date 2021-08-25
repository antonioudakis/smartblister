from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MonitoringRequestForm, PatientSearchForm, PrescriptionAddForm
from django.core.mail import send_mail
from users.models import PatientProfile, DoctorProfile, UserProfile
from doctor.models import MonitoringRequest, Prescription
from pharmacist.models import BlisterAction,BlisterPrescription
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def monitoring_request(request):
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
		'title':'Αίτημα πρόσβασης smartblister',
		'form':form,
		'users':users
	}
	return render(request,'doctor/monitoring_request.html', context)

@login_required
def monitoring_request_send(request):
	if request.method == 'POST':
		import json, hashlib

		with open('/etc/config.json') as config_file:
			config = json.load(config_file)

		EMAIL_HOST_USER = config.get('EMAIL_USER')
		patientmainprofile = UserProfile.objects.get(id=request.POST['patient'])
		try:
			patient = PatientProfile.objects.get(user=patientmainprofile.user)
			doctor = DoctorProfile.objects.get(user=request.user.id)
			date_requested = timezone.now()
			pre_token = str(doctor.id)+str(patient.id)+str(date_requested)
			token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
			req = MonitoringRequest.objects.create(doctor=doctor,patient=patient,date_requested=date_requested,token=token)
			req.save()
			host = config.get('HOST_URL')
			subject = 'Smartblister - Αίτηση πρόσβασης στα στοιχεία του smartblister'
			sender = EMAIL_HOST_USER
			recipient = patient.user.email
			plain_message = 'Ο ιατρός '+ request.user.last_name + ' '+ request.user.first_name + ' με ειδικότητα ' + doctor.speciality +' έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο; '+host+'smartblister/doctor/monitoring_accept/'+token
			html_message = '<p>Ο ιατρός <b>'+ request.user.last_name + ' '+ request.user.first_name + '</b> με ειδικότητα <b>' + doctor.speciality +"</b> έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο;</p><p><a href='"+host+"smartblister/doctor/monitoring_accept/"+token+"/'>"+host+"smartblister/doctor/monitoring_accept/"+token+"/</a></p>"
			send_mail(subject,plain_message, sender, [recipient,], fail_silently=False,html_message=html_message)
			messages.success(request,f'Έχει αποσταλεί στον ασθενή με όνομα {patient.user.last_name} {patient.user.first_name} αίτημα μέσω ηλεκτρονικού μηνύματος για εξουσιοδότηση πρόσβασης στα στοιχεία του smartblister που διαθέτει. Θα έχετε πρόσβαση στα σχετικά στοιχεία του ασθενούς όταν γίνει αποδοχή του αιτήματός σας. Αμέσως μετά την αποδοχή του αιτήματος θα λάβετε την σχετική ενημέρωση μέσω ηλεκτρονικού μηνύματος.')
		except PatientProfile.DoesNotExist:
			messages.warning(request,f'Δεν υπάρχει καταχωρημένος ασθενής με το στοιχεία που δηλώσατε')
		
	else:
		messages.warning(request,f'Θσ πρέπει να συνδεθείτε ως ιατρός και να αποστείλετε αίτημα πρόσβασης σε στοιχεία smartblister του ασθενούς που θα έχετε πρώτα αναζητήσει.')

	return render(request,'dashboard/index.html')

def monitoring_accept(request,token):
	req = MonitoringRequest.objects.filter(token=token).first()
	if req:
		doctor = req.doctor
		patient = req.patient
		patient.doctor = doctor
		patient.save()
		req.date_accepted = timezone.now()
		req.save()
		import json

		with open('/etc/config.json') as config_file:
			config = json.load(config_file)

		EMAIL_HOST_USER = config.get('EMAIL_USER')
		subject = 'Smartblister - Αποδοχή αιτήματος πρόσβασης στα στοιχεία του smartblister'
		sender = EMAIL_HOST_USER
		recipient = doctor.user.email
		plain_message = 'Ο ασθενής '+patient.user.last_name+' '+patient.user.first_name+' έχει αποδεχθεί το αίτημά σας για πρόσβαση στα στοιχεία του smartblister που διαθέτει'
		html_message = 'Ο ασθενής <b>'+patient.user.last_name+' '+patient.user.first_name+'</b> έχει αποδεχθεί το αίτημά σας για πρόσβαση στα στοιχεία του smartblister που διαθέτει.'
		send_mail(subject,plain_message, sender, [recipient,], fail_silently=False,html_message=html_message)
		messages.success(request,f'Έχετε αποδεχθεί το αίτημα πρόσβασης του ιατρού με όνομα {doctor.user.last_name} {doctor.user.first_name} στα στοιχεία του smartblister που διαθέτετε. Μπορείτε οποιαδήποτε στιγμή να αναιρέσετε την ενέργεια αυτή πηγαίνοντας στο προφίλ σας αφού πρώτα συνδεθείτε στο σύστημα.')
	else:
		messages.warning(request,f'Τα στοιχεία δεν είναι έγκυρα.')

	context = {
		'title':'Αίτημα πρόσβασης smartblister',
		'role':'patient',
	}
	return render(request,'dashboard/index.html',context)

@login_required
def prescription(request):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		form1 = PrescriptionAddForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			try:
				patient = PatientProfile.objects.get(user__userprofile__amka=amka)
				prescriptions = patient.prescription_set.all().order_by('-date_issued')
			except PatientProfile.DoesNotExist:
				patient = None
				prescriptions = None
		else:
			patient = None
			prescription = None
	else:
		form = PatientSearchForm()
		form1 = PrescriptionAddForm()
		patient = None
		prescriptions = None


	context = {
		'title':'Συνταγογράφηση',
		'form':form,
		'form1':form1,
		'patient':patient,
		'prescriptions': prescriptions
	}
	
	return render(request,'doctor/prescription.html', context)

"""@login_required
def actions(request):
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
	
	return render(request,'doctor/prescription_list.html', context)"""

@login_required
def actions(request,prescription_id):
	try:
		actions = BlisterAction.objects.filter(blisterPrescription__prescription__id=prescription_id).order_by('-date_removed')
		prescription = Prescription.objects.get(id=prescription_id)
		patient = prescription.patient
	except BlisterPrescription.DoesNotExist:
		actions = None
		prescription = None
		patient = None

	context = {
		'title':'Φαρμακευτική Συνέπεια',
		'actions':actions,
		'prescription':prescription,
		'patient':patient
	}
	
	return render(request,'doctor/action_list.html', context)



@login_required
def chargedPrescriptions(request,patient_id):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		form1 = PrescriptionAddForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			try:
				patient = PatientProfile.objects.get(user__userprofile__amka=amka)
				prescriptions = patient.prescription_set.all().order_by('-date_issued')
			except PatientProfile.DoesNotExist:
				patient = None
				prescriptions = None
		else:
			patient = None
			prescriptions = None
	else:
		form = PatientSearchForm()
		form1 = PrescriptionAddForm()
		try:
			patient = PatientProfile.objects.get(id=patient_id)
			prescriptions = patient.prescription_set.all().order_by('-date_issued')
		except PatientProfile.DoesNotExist:
			patient = None
			blisters = None


	context = {
		'title':'Συνταγογράφηση',
		'form':form,
		'form1':form1,
		'patient':patient,
		'prescriptions': prescriptions
	}
	
	return render(request,'doctor/prescription.html', context)

@login_required
def deletePrescription(request,prescription_id):
	try:
		prescription = Prescription.objects.get(id=prescription_id)
		patient = prescription.patient
		prescription.delete()
		return redirect('doctor:chargedPrescriptions', patient_id=patient.id)
	except Prescription.DoesNotExist:
		messages.warning(request,f'Δεν υπάρχει συνταγή με τα στοιχεία που δώσατε')
		return redirect('doctor:prescription')

@login_required
def addPrescription(request,patient_id):
	if request.method == 'POST':
		form = PrescriptionAddForm(request.POST)
		patient = PatientProfile.objects.get(id=patient_id)
		if form.is_valid():
			print("valid form")
			prescription = form.save(commit=False)
			prescription.patient = patient
			prescription.doctor = request.user.doctorprofile
			prescription.save()
			prescriptions = patient.prescription_set.all().order_by('-date_issued')
			#messages.success(request,f'To blister αποθηκεύτηκε')
		else:
			print("not valid form")
			print(form.errors)

	else:
		print("not posted")
		form = PrescriptionAddForm()
		patient = PatientProfile.objects.get(id=patient_id)
		prescriptions = patient.prescription_set.all()


	context = {
		'title':'Συνταγογράφηση Ασθενούς',
		'form':form,
		'patient':patient,
		'prescriptions': prescriptions
	}
	
	return redirect('doctor:chargedPrescriptions', patient_id=patient.id)

