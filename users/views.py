from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm

def register(request):
	return render(request,'users/register.html', {'title':'Εγγραφή'})

def register_doctor(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'O λογαριασμός δημιουργήθηκε με όνομα χρήστη {username} !')
			return redirect('users:login')
	else:
		form = UserRegisterForm()
	return render(request,'users/register_doctor.html', {'title':'Εγγραφή Ιατρού','form':form})

@login_required
def profile(request):
	return render(request,'users/profile.html', {'title':'Προφίλ'})
