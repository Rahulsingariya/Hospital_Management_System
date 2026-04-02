from django.db import models


class LabTest(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    normal_range = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    turnaround_hours = models.IntegerField(default=24)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.code})'


class LabOrder(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Ordered'), ('sample_collected', 'Sample Collected'),
        ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='lab_orders')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Lab Order - {self.patient.full_name} ({self.ordered_date.date()})'

    class Meta:
        ordering = ['-ordered_date']


class LabResult(models.Model):
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result_value = models.CharField(max_length=200)
    is_normal = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.test.name}: {self.result_value}'
