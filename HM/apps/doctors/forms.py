from django import forms
from .models import Doctor, Department, DoctorSchedule, Specialization


class DoctorForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="-- Select Department --",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px; background-color: #fff;'
        })
    )
    
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        empty_label="-- Select Specialization --",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px; background-color: #fff;'
        })
    )

    class Meta:
        model = Doctor
        exclude = ['doctor_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name of doctor',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'user': forms.Select(attrs={
                'class': 'form-select',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MBBS, MD, BDS',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'consultation_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Consultation fee',
                'step': '0.01',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Professional summary or bio',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px; font-family: inherit;'
            }),
            'joining_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'padding: 10px 15px; font-size: 15px; border: 2px solid #e0e0e0; border-radius: 6px;'
            }),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head_doctor': forms.Select(attrs={'class': 'form-select'}),
        }


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        exclude = ['doctor']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'max_appointments': forms.NumberInput(attrs={'class': 'form-control'}),
        }
