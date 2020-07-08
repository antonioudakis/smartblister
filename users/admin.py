from django.contrib import admin
from users.models import UserProfile, DoctorProfile

admin.site.register(UserProfile)
admin.site.register(DoctorProfile)