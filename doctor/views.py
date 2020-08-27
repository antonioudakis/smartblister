from django.shortcuts import render, redirect
from .forms import MonitoringRequestForm
from django.core.mail import send_mail

def monitoring_request(request):
	if request.method == 'POST':
		form = MonitoringRequestForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			import os
			EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
			send_mail('Subject here','Here is the message.', EMAIL_HOST_USER, [email], fail_silently=False,)
			return redirect('dashboard:index')


	else:
		form = MonitoringRequestForm()

	context = {
		'form':form,
	}

	return render(request,'doctor/monitoring_request.html', context)
