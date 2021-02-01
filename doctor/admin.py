from django.contrib import admin
from doctor.models import MonitoringRequest, Prescription, Frequency, Duration

admin.site.register(MonitoringRequest)
admin.site.register(Prescription)
admin.site.register(Frequency)
admin.site.register(Duration)

