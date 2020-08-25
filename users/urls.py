from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

app_name = 'users'

urlpatterns = [
	path('registration/',views.registration, name='registration'),
	path('register/doctor/',views.register_doctor, name='register_doctor'),
	path('register/pharmacist/',views.register_pharmacist, name='register_pharmacist'),
	path('register/pharmacy/',views.register_pharmacy, name='register_pharmacy'),
	path('register/patient/',views.register_patient, name='register_patient'),
	path('profile',views.profile, name='profile'),
]