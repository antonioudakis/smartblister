from django.urls import path
from pharmacist import views


app_name = 'pharmacist'

urlpatterns = [
	path('charge/<int:user_id>/',views.charge, name='charge'),
	path('charge/new',views.charge_init, name='charge_init'),
]