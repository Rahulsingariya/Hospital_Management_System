from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Patient, MedicalRecord, VitalSign
from .forms import PatientForm, MedicalRecordForm, VitalSignForm


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query) |
            Q(phone__icontains=query)
        )
    if status:
        patients = patients.filter(status=status)

    paginator = Paginator(patients, 15)
    page = request.GET.get('page', 1)
    patients = paginator.get_page(page)

    return render(request, 'patients/patient_list.html', {
        'patients': patients, 'query': query, 'status': status
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = patient.medical_records.all()[:5]
    vitals = patient.vitals.all()[:5]
    appointments = patient.appointments.all()[:5]
    invoices = patient.invoices.all()[:5]
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'records': records,
        'vitals': vitals,
        'appointments': appointments,
        'invoices': invoices,
    })


@login_required
def patient_create(request):
    form = PatientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        patient = form.save()
        messages.success(request, f'Patient {patient.full_name} registered successfully! ID: {patient.patient_id}')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Register New Patient'})


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST or None, request.FILES or None, instance=patient)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Patient updated successfully!')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Edit Patient', 'patient': patient})


@login_required
def add_medical_record(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = MedicalRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        record.patient = patient
        record.save()
        messages.success(request, 'Medical record added!')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/medical_record_form.html', {'form': form, 'patient': patient})


@login_required
def add_vital_signs(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    form = VitalSignForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vital = form.save(commit=False)
        vital.patient = patient
        vital.recorded_by = request.user
        vital.save()
        messages.success(request, 'Vital signs recorded!')
        return redirect('patients:detail', pk=patient.pk)
    return render(request, 'patients/vital_form.html', {'form': form, 'patient': patient})
