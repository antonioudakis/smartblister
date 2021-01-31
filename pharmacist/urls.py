from django.urls import path
from pharmacist import views


app_name = 'pharmacist'

urlpatterns = [
	path('blister/',views.blister, name='blister'),
	path('blister/patient/<int:patient_id>/',views.chargedBlisters, name='chargedBlisters'),
	path('blister/patient/add/<int:patient_id>/',views.addBlister, name='addBlister'),
	path('blister/delete/<int:blister_id>/',views.deleteBlister, name='deleteBlister'),
	path('blister/prescription/<int:patient_id>/<int:blister_id>/',views.blisterPrescription, name='blisterPrescription'),
	path('charge/<int:user_id>/',views.chargeBlister, name='chargeBlister'),
	path('charge/new',views.chargeBlister_init, name='chargeBlister_init'),
]