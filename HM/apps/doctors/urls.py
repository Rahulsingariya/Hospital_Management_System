from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='list'),
    path('create/', views.doctor_create, name='create'),
    path('<int:pk>/', views.doctor_detail, name='detail'),
    path('<int:pk>/edit/', views.doctor_edit, name='edit'),
    path('departments/', views.department_list, name='departments'),
]
