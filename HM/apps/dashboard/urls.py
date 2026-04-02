from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', lambda request: __import__('django.shortcuts', fromlist=['redirect']).redirect('dashboard:index'), name='home'),
    path('dashboard/', views.index, name='index'),
]
