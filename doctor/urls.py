from django.urls import path
from django.contrib.auth import views as auth_views
from doctor import views


app_name = 'doctor'

urlpatterns = [
	path('monitoring_request/',views.monitoring_request, name='monitoring_request'),
	#path('monitoring_request_complete/<str:token>/',views.monitoring_request_complete, name='monitoring_request_complete'),
	path('monitoring_accept/<str:token>/',views.monitoring_accept, name='monitoring_accept'),
]