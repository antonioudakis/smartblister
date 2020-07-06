from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def register(request):
	return render(request,'users/register.html', {'title':'Εγγραφή'})
