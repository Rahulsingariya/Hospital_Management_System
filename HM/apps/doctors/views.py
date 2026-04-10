from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Doctor, Department, DoctorSchedule
from .forms import DoctorForm, DepartmentForm, DoctorScheduleForm


@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    doctors = Doctor.objects.select_related('user', 'department', 'specialization').all()

    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(doctor_id__icontains=query) |
            Q(specialization__name__icontains=query)
        )
    if dept:
        doctors = doctors.filter(department_id=dept)

    departments = Department.objects.all()
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors, 'departments': departments,
        'query': query, 'selected_dept': dept
    })


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    schedules = doctor.schedules.filter(is_active=True)
    appointments = doctor.appointments.all()[:10]
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor, 'schedules': schedules, 'appointments': appointments
    })


@login_required
def doctor_create(request):
    form = DoctorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        doctor = form.save()
        messages.success(request, f'{doctor.full_name} registered successfully!')
        return redirect('doctors:detail', pk=doctor.pk)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add Doctor'})


@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST or None, instance=doctor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Doctor updated successfully!')
        return redirect('doctors:detail', pk=doctor.pk)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Edit Doctor', 'doctor': doctor})


@login_required
def department_list(request):
    departments = Department.objects.prefetch_related('doctor_set').all()
    return render(request, 'doctors/department_list.html', {'departments': departments})


@login_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dept = form.save()
        messages.success(request, f'Department "{dept.name}" created successfully!')
        return redirect('doctors:departments')
    return render(request, 'doctors/department_form.html', {'form': form, 'title': 'Add Department'})
