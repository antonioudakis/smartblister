from django.contrib import admin
from .models import Blister, BlisterPrescription, BlisterAction

admin.site.register(Blister)
admin.site.register(BlisterPrescription)
admin.site.register(BlisterAction)
