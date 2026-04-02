from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('patients/', include('apps.patients.urls')),
    path('doctors/', include('apps.doctors.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('billing/', include('apps.billing.urls')),
    path('pharmacy/', include('apps.pharmacy.urls')),
    path('lab/', include('apps.lab.urls')),
    path('api/', include('apps.dashboard.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom admin headers
admin.site.site_header = 'MediCare Hospital Admin'
admin.site.site_title = 'MediCare Admin'
admin.site.index_title = 'Hospital Management'
