from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),
    path('create/', views.patient_create, name='create'),
    path('<int:pk>/', views.patient_detail, name='detail'),
    path('<int:pk>/edit/', views.patient_edit, name='edit'),
    path('<int:patient_pk>/records/add/', views.add_medical_record, name='add_record'),
    path('<int:patient_pk>/vitals/add/', views.add_vital_signs, name='add_vitals'),
]
