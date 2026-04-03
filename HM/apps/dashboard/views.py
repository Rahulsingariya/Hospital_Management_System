from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.appointments.models import Appointment
from apps.billing.models import Invoice
from apps.pharmacy.models import Medicine
import json


@login_required
def index(request):
    today = timezone.now().date()
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Stats
    total_patients = Patient.objects.filter(status='active').count()
    total_doctors = Doctor.objects.filter(availability__in=['available', 'busy']).count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    monthly_revenue = Invoice.objects.filter(
        status='paid',
        issue_date__month=current_month,
        issue_date__year=current_year
    ).aggregate(total=Sum('total'))['total'] or 0

    # Today's appointments
    appointments_today = Appointment.objects.filter(
        appointment_date=today
    ).select_related('patient', 'doctor__user').order_by('appointment_time')[:8]

    # Recent patients
    recent_patients = Patient.objects.order_by('-registered_at')[:5]

    # Low stock medicines
    low_stock = Medicine.objects.filter(
        quantity_in_stock__lte=10, is_active=True
    )[:5]

    # Appointment status summary
    status_summary = Appointment.objects.filter(
        appointment_date=today
    ).values('status').annotate(count=Count('id'))

    # Monthly revenue chart (last 6 months)
    revenue_data = []
    for i in range(5, -1, -1):
        from dateutil.relativedelta import relativedelta
        month_date = timezone.now().date() - relativedelta(months=i)
        rev = Invoice.objects.filter(
            status='paid',
            issue_date__month=month_date.month,
            issue_date__year=month_date.year
        ).aggregate(total=Sum('total'))['total'] or 0
        revenue_data.append({
            'month': month_date.strftime('%b %Y'),
            'revenue': float(rev)
        })

    # Pending invoices
    pending_invoices = Invoice.objects.filter(
        status__in=['sent', 'partial']
    ).select_related('patient').order_by('-created_at')[:5]

    # Convert to JSON for template
    revenue_data_json = json.dumps(revenue_data, cls=DjangoJSONEncoder)
    status_summary_json = json.dumps(list(status_summary), cls=DjangoJSONEncoder)

    return render(request, 'dashboard/index.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'monthly_revenue': monthly_revenue,
        'appointments_today': appointments_today,
        'recent_patients': recent_patients,
        'low_stock': low_stock,
        'status_summary': list(status_summary),
        'revenue_data': revenue_data,
        'status_summary_json': status_summary_json,
        'revenue_data_json': revenue_data_json,
        'pending_invoices': pending_invoices,
    })


@login_required
def api_stats(request):
    """API endpoint for real-time dashboard stats"""
    today = timezone.now().date()
    data = {
        'patients': Patient.objects.filter(status='active').count(),
        'doctors': Doctor.objects.filter(availability='available').count(),
        'appointments': Appointment.objects.filter(appointment_date=today).count(),
        'pending_invoices': Invoice.objects.filter(status__in=['sent', 'partial']).count(),
    }
    return JsonResponse(data)
