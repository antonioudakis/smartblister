from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages

def index(request):
	return render(request,'dashboard/index.html')