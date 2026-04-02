from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LabTest, LabOrder, LabResult


@login_required
def lab_order_list(request):
    orders = LabOrder.objects.select_related('patient', 'doctor__user').all()
    return render(request, 'lab/order_list.html', {'orders': orders})


@login_required
def lab_order_detail(request, pk):
    order = get_object_or_404(LabOrder, pk=pk)
    return render(request, 'lab/order_detail.html', {'order': order})


@login_required
def test_list(request):
    tests = LabTest.objects.all()
    return render(request, 'lab/test_list.html', {'tests': tests})


@login_required
def update_order_status(request, pk):
    order = get_object_or_404(LabOrder, pk=pk)
    status = request.POST.get('status')
    if status in dict(LabOrder.STATUS_CHOICES):
        order.status = status
        if status == 'processing':
            order.processed_by = request.user
        order.save()
        messages.success(request, f'Lab order status updated to {status}.')
    return redirect('lab:order_detail', pk=pk)
