from django.shortcuts import render, redirect
from .forms import MonitoringRequestForm
from django.core.mail import send_mail
from users.models import PatientProfile, DoctorProfile
from doctor.models import MonitoringRequest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404

def monitoring_request(request):
	if request.method == 'POST':
		form = MonitoringRequestForm(request.POST)
		if form.is_valid():
			import os, hashlib
			EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
			user = User.objects.filter(id=request.user.id).first()
			patient = form.cleaned_data.get('patient')
			doctor = DoctorProfile.objects.filter(user=request.user.id).first()
			print(doctor)
			date_requested = timezone.now()
			pre_token = str(doctor.id)+str(patient.id)+str(date_requested)
			token = hashlib.sha256(pre_token.encode('utf-8')).hexdigest()
			#request = MonitoringRequest.objects.create(doctor=doctor,patient=patient,date_requested=date_requested,token=token,accepted=False)
			req = MonitoringRequest(doctor=doctor,patient=patient,date_requested=date_requested,token=token,accepted=False)
			req.save()
			subject = 'Smartblister - Αίτηση Πρόσβασης στα στοιχεία του smartblister'
			sender = EMAIL_HOST_USER
			recipient = patient.user.email
			plain_message = 'Ο ιατρός '+ request.user.last_name + ' '+ request.user.first_name + ' με ειδικότητα ' + doctor.speciality +' έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο; http://localhost:8000/doctor/monitoring_accept/'+token
			html_message = '<p>Ο ιατρός <b>'+ request.user.last_name + ' '+ request.user.first_name + '</b> με ειδικότητα <b>' + doctor.speciality +"</b> έχει αιτηθεί πρόσβαση στα στοιχεία του smartblister σας. Αν Θέλετε να κάνετε αποδοχή της αίτησης κάντε κλικ στον παρακάτω σύνδεσμο;</p><p><a href='http://localhost:8000/doctor/monitoring_accept/"+token+"/'>http://localhost:8000/doctor/monitoring_accept/"+token+"/</a></p>"
			send_mail(subject,plain_message, sender, [recipient,], fail_silently=False,html_message=html_message)
			#messages.success(request,f'O λογαριασμός δημιουργήθηκε. Μπορείτε τώρα να συνδεθείτε')
			return redirect('dashboard:index')


	else:
		form = MonitoringRequestForm()

	context = {
		'form':form,
	}

	return render(request,'doctor/monitoring_request.html', context)

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

