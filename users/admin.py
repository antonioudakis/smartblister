from django.contrib import admin
from users.models import UserProfile, DoctorProfile, PharmacistProfile, PharmacyProfile, PatientProfile

admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(PharmacistProfile)
admin.site.register(PharmacyProfile)
admin.site.register(PatientProfile)