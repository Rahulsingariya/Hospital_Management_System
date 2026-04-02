from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemFormSet


@login_required
def invoice_list(request):
    status = request.GET.get('status', '')
    query = request.GET.get('q', '')
    invoices = Invoice.objects.select_related('patient').all()

    if status:
        invoices = invoices.filter(status=status)
    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query)
        )

    total_revenue = Invoice.objects.filter(status='paid').aggregate(t=Sum('total'))['t'] or 0
    pending_invoices = Invoice.objects.filter(status__in=['sent', 'partial'])
    pending_amount = sum(inv.balance_due for inv in pending_invoices) or 0

    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices, 'total_revenue': total_revenue,
        'pending_amount': pending_amount, 'status': status, 'query': query,
    })


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    form = InvoiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        invoice = form.save(commit=False)
        invoice.created_by = request.user
        invoice.save()
        messages.success(request, f'Invoice {invoice.invoice_number} created!')
        return redirect('billing:detail', pk=invoice.pk)
    return render(request, 'billing/invoice_form.html', {'form': form})


@login_required
def mark_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'paid'
    invoice.amount_paid = invoice.total
    invoice.save()
    messages.success(request, f'Invoice {invoice.invoice_number} marked as paid!')
    return redirect('billing:detail', pk=pk)
