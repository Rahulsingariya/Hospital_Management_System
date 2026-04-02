from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    today = timezone.now().date()
    status = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    query = request.GET.get('q', '')

    appointments = Appointment.objects.select_related('patient', 'doctor__user').all()

    if status:
        appointments = appointments.filter(status=status)
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(appointment_id__icontains=query) |
            Q(doctor__user__first_name__icontains=query)
        )

    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'today_count': today_appointments,
        'status': status, 'query': query,
    })


@login_required
def appointment_create(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.created_by = request.user
        appt.save()
        messages.success(request, f'Appointment {appt.appointment_id} booked successfully!')
        return redirect('appointments:list')
    return render(request, 'appointments/appointment_form.html', {'form': form, 'title': 'Book Appointment'})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    status = request.POST.get('status')
    if status in dict(Appointment.STATUS_CHOICES):
        appointment.status = status
        appointment.save()
        messages.success(request, f'Appointment status updated to {status}.')
    return redirect('appointments:detail', pk=pk)
