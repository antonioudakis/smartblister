from django.contrib import admin
from .models import Blister, Prescription, BlisterPrescription

admin.site.register(Blister)
admin.site.register(Prescription)
admin.site.register(BlisterPrescription)
