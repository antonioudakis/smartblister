from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
	path('register/',views.register, name='register'),
	path('register/doctor',views.register_doctor, name='register_doctor'),
]