from django.contrib import admin
from users.models import UserProfile, DoctorProfile, PharmacistProfile, PharmacyProfile

admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(PharmacistProfile)
admin.site.register(PharmacyProfile)