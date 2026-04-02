from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from .models import Medicine, Prescription, MedicineCategory


@login_required
def medicine_list(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.select_related('category').filter(is_active=True)
    if query:
        medicines = medicines.filter(Q(name__icontains=query) | Q(generic_name__icontains=query))

    low_stock = Medicine.objects.filter(quantity_in_stock__lte=F('reorder_level'), is_active=True).count()
    return render(request, 'pharmacy/medicine_list.html', {
        'medicines': medicines, 'query': query, 'low_stock': low_stock
    })


@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.select_related('patient', 'doctor__user').all()
    return render(request, 'pharmacy/prescription_list.html', {'prescriptions': prescriptions})


@login_required
def dispense_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        prescription.status = 'dispensed'
        prescription.dispensed_by = request.user
        from django.utils import timezone
        prescription.dispensed_at = timezone.now()
        prescription.save()
        messages.success(request, 'Prescription dispensed successfully!')
    return redirect('pharmacy:prescriptions')
