from django.urls import path
from django.contrib.auth import views as auth_views
from doctor import views


app_name = 'doctor'

urlpatterns = [
	path('monitoring_request/',views.monitoring_request, name='monitoring_request'),
]