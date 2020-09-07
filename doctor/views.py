from django.shortcuts import render, redirect
from .forms import MonitoringRequestForm, PatientSearchForm
from django.core.mail import send_mail
from users.models import PatientProfile, DoctorProfile, UserProfile
from doctor.models import MonitoringRequest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404

def monitoring_request(request):
	if request.method == 'POST':
		form = PatientSearchForm(request.POST)
		if form.is_valid():
			amka = form.cleaned_data['amka']
			users = UserProfile.objects.filter(amka__startswith=amka)
			users = users.filter(is_patient=True)
			#try:
				
				#users = users.filter(last_name=last_name)
			#except:
			#	users = None
			
			#messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			#return redirect('dashboard:index')
			


	else:
		form = PatientSearchForm()
		users = None

	context = {
		'form':form,
		'users':users
	}
	return render(request,'doctor/monitoring_request.html', context)

def monitoring_request_send(request):
	if request.method == 'POST':
		import os, hashlib
		EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
		patientmainprofile = UserProfile.objects.get(id=request.POST['patient'])
		#userprofile = get_object_or_404(UserProfile, id=request.POST['patient'])
		patient = PatientProfile.objects.get(user=patientmainprofile.user)
		doctor = DoctorProfile.objects.get(user=request.user.id)
		date_requested = timezone.now()
		pre_token = str(doctor.id)+str(patient.id)+str(date_requested)
		token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
		req = MonitoringRequest.objects.create(doctor=doctor,patient=patient,date_requested=date_requested,token=token,accepted=False)
		req.save()
		subject = 'Smartblister - Αίτηση Πρόσβασης στα στοιχεία του smartblister'
		sender = EMAIL_HOST_USER
		recipient = patient.user.email
		plain_message = 'Ο ιατρός '+ request.user.last_name + ' '+ request.user.first_name + ' με ειδικότητα ' + doctor.speciality +' έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο; http://localhost:8000/doctor/monitoring_accept/'+token
		html_message = '<p>Ο ιατρός <b>'+ request.user.last_name + ' '+ request.user.first_name + '</b> με ειδικότητα <b>' + doctor.speciality +"</b> έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο;</p><p><a href='http://localhost:8000/doctor/monitoring_accept/"+token+"/'>http://localhost:8000/doctor/monitoring_accept/"+token+"/</a></p>"
		send_mail(subject,plain_message, sender, [recipient,], fail_silently=False,html_message=html_message)

		context = {
			'message':'Έχει αποσταλεί ηλεκτρονικό μήνυμα (email) στον '+patient.user.last_name+' '+patient.user.first_name+' αίτημα για να έχετε πρόσβαση στα στοιχεία του smartblister. Θα έχετε πρόσβαση στα σχετικά στοιχεία αμέσως μόλις κάνει αποδοχή.',
		}
	else:
		context = None

	return render(request,'doctor/info.html',context)

def monitoring_accept(request,token):
	req = get_object_or_404(MonitoringRequest, token=token)
	doctor = req.doctor
	patient = req.patient
	patient.doctor = doctor
	patient.save()
	context = {
		'title':'Εγγραφή Φαρμακοποιού',
		'role':'pharmacist',
	}
	return render(request,'doctor/monitoring_accept.html',context)

