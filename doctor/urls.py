from django.urls import path
from django.contrib.auth import views as auth_views
from doctor import views


app_name = 'doctor'

urlpatterns = [
	path('monitoring_request/',views.monitoring_request, name='monitoring_request'),
	path('monitoring_request/send/',views.monitoring_request_send, name='monitoring_request_send'),
	#path('monitoring_request_complete/<str:token>/',views.monitoring_request_complete, name='monitoring_request_complete'),
	path('monitoring_accept/<str:token>/',views.monitoring_accept, name='monitoring_accept'),
	path('prescription/',views.prescription, name='prescription'),
	path('prescription/patient/<int:patient_id>/',views.chargedPrescriptions, name='chargedPrescriptions'),
	path('prescription/patient/add/<int:patient_id>/',views.addPrescription, name='addPrescription'),
	path('prescription/delete/<int:prescription_id>/',views.deletePrescription, name='deletePrescription'),
	path('patient/prescription/action_list/<int:prescription_id>/',views.actions, name='actions'),
]