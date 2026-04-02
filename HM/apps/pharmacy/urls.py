from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.medicine_list, name='medicines'),
    path('prescriptions/', views.prescription_list, name='prescriptions'),
    path('prescriptions/<int:pk>/dispense/', views.dispense_prescription, name='dispense'),
]
