from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    AVAILABILITY_CHOICES = [('available', 'Available'), ('busy', 'Busy'), ('off', 'Off Duty')]

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=200, default='')
    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    bio = models.TextField(blank=True)
    joining_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            count = Doctor.objects.count() + 1
            self.doctor_id = f'DOC-{count:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Dr. {self.user.get_full_name()} - {self.specialization}'

    @property
    def full_name(self):
        return f'Dr. {self.user.get_full_name()}'

    class Meta:
        ordering = ['user__first_name']


class DoctorSchedule(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_appointments = models.IntegerField(default=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.doctor.full_name} - {self.get_day_of_week_display()}'

    class Meta:
        unique_together = ['doctor', 'day_of_week']
        ordering = ['day_of_week']
