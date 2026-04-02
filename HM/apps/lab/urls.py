from django.urls import path
from . import views

app_name = 'lab'

urlpatterns = [
    path('', views.lab_order_list, name='orders'),
    path('tests/', views.test_list, name='tests'),
    path('<int:pk>/', views.lab_order_detail, name='order_detail'),
    path('<int:pk>/status/', views.update_order_status, name='update_status'),
]
