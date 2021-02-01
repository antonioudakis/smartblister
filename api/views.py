from django.shortcuts import render
#from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer, ChargeSerializer, BlisterSerializer, BlisterPrescriptionSerializer, BlisterActionSerializer
from .models import Task
from pharmacist.models import Blister, BlisterPrescription, BlisterAction

@api_view(['GET'])
def apiOverview(request):
	#return JsonResponse("API BASE POINT", safe=False)
	api_urls = {
		#'List':'/task-list/',
		#'Detail View':'/tast-detail/<str:pk>/',
		#'Create':'/task-create/',
		#'Update':'/task-update/<str:pk>/',
		#'Delete':'/task-delete/<str:pk>/',
		'Service':'/service/',
		'Status':'/status/<str:pk>/',
		'PillRemoved':'/pillRemoved/<str:serial>/',
	}

	#return JsonResponse("API BASE POINT", safe=False)
	return Response(api_urls)

@api_view(['GET'])
def service(request):
	return Response("Smartblister Rest Service is Up and Running", status=200)

@api_view(['GET'])
def status(request, pk):
	try:
		blister = Blister.objects.get(serial=pk)
		blisterPrescription = BlisterPrescription.objects.get(blister=blister)
		serializer = BlisterPrescriptionSerializer(blisterPrescription, many=False)
		return Response(serializer.data, status=200)
	except blister.DoesNotExist:
		return Response("Not found", status=404)
	except blisterPrescription.DoesNotExist:
		return Response("Not found", status=404)

@api_view(['POST'])
def pillRemoved(request, serial):
	blister = Blister.objects.get(serial=serial)
	blisterPrescription = BlisterPrescription.objects.get(blister=blister)
	p = BlisterAction(blisterPrescription=blisterPrescription)
	p.save()
	#serializer1 = BlisterPrescriptionSerializer(blisterPrescription, many=False)
	#serializer = BlisterActionSerializer(data=serializer1)
	
	#if serializer.is_valid():
	#	print("valid data")
	#	serializer.save()
	#else:
	#	print("not valid")
	#	print(serializer)

	#return Response(serializer.data, status=201)
	return Response("Η αφαίρεση δισκίου καταχωρήθηκε", status=201)
	

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all()
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def taskUpdate(request, pk):
	try:
		task = Task.objects.get(id=pk)
		serializer = TaskSerializer(instance=task, data=request.data)

		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data)
	except Task.DoesNotExist:
		return Response("Not found - Nothing to Update", status=404)

@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(task, many=False)
	task.delete()

	#return Response('Item successfully delete!')
	return Response(serializer.data, status=status.HTTP_200_OK)
