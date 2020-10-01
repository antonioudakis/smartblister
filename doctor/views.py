from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MonitoringRequestForm, PatientSearchForm
from django.core.mail import send_mail
from users.models import PatientProfile, DoctorProfile, UserProfile
from doctor.models import MonitoringRequest
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
		import os, hashlib
		EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
		patientmainprofile = UserProfile.objects.get(id=request.POST['patient'])
		try:
			patient = PatientProfile.objects.get(user=patientmainprofile.user)
			doctor = DoctorProfile.objects.get(user=request.user.id)
			date_requested = timezone.now()
			pre_token = str(doctor.id)+str(patient.id)+str(date_requested)
			token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
			req = MonitoringRequest.objects.create(doctor=doctor,patient=patient,date_requested=date_requested,token=token)
			req.save()
			subject = 'Smartblister - Αίτηση πρόσβασης στα στοιχεία του smartblister'
			sender = EMAIL_HOST_USER
			recipient = patient.user.email
			plain_message = 'Ο ιατρός '+ request.user.last_name + ' '+ request.user.first_name + ' με ειδικότητα ' + doctor.speciality +' έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο; http://localhost:8000/doctor/monitoring_accept/'+token
			html_message = '<p>Ο ιατρός <b>'+ request.user.last_name + ' '+ request.user.first_name + '</b> με ειδικότητα <b>' + doctor.speciality +"</b> έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο;</p><p><a href='https://smartblister.gr/doctor/monitoring_accept/"+token+"/'>https://smartblister.gr/doctor/monitoring_accept/"+token+"/</a></p>"
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
		import os
		EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
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

