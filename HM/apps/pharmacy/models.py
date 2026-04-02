from django.db import models
from django.utils import timezone


class MedicineCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, default='tablets')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False

    class Meta:
        ordering = ['name']


class Prescription(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('dispensed', 'Dispensed'), ('cancelled', 'Cancelled')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    dispensed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    dispensed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Prescription - {self.patient.full_name} ({self.issued_date})'


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f'{self.medicine.name} - {self.dosage}'
