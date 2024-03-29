from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name='api-overview'),
	path('task-list/', views.taskList, name='task-list'),
	path('task-detail/<str:pk>/', views.taskDetail, name='task-detail'),
	path('task-create/', views.taskCreate, name='task-create'),
	path('task-update/<str:pk>/', views.taskUpdate, name='task-update'),
	path('task-delete/<str:pk>/', views.taskDelete, name='task-delete'),
	path('status/<str:pk>/', views.status, name='status'),
	path('service/', views.service, name='service'),
	path('pillRemoved/<str:serial>/', views.pillRemoved, name='pillRemoved'),
	path('actions/<int:prescription_id>/', views.actions, name='actions'),
	path('detailedActions/<int:prescription_id>/', views.detailedActions, name='detailedActions'),
]