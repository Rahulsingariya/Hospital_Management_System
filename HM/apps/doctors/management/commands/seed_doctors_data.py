from django.core.management.base import BaseCommand
from django.core.management import call_command
from apps.doctors.models import Department, Specialization


class Command(BaseCommand):
    help = 'Seed departments and specializations data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular care'},
            {'name': 'Neurology', 'description': 'Nervous system and brain care'},
            {'name': 'Orthopedics', 'description': 'Bone and joint care'},
            {'name': 'Dermatology', 'description': 'Skin care'},
            {'name': 'Pediatrics', 'description': 'Children\'s care'},
            {'name': 'General Medicine', 'description': 'General medical services'},
            {'name': 'Gynecology', 'description': 'Women\'s health'},
            {'name': 'Oncology', 'description': 'Cancer treatment'},
            {'name': 'Surgery', 'description': 'Surgical services'},
            {'name': 'Psychiatry', 'description': 'Mental health services'},
        ]
        
        for dept in departments_data:
            obj, created = Department.objects.get_or_create(
                name=dept['name'],
                defaults={'description': dept['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created department: {dept["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'✓ Department already exists: {dept["name"]}'))
        
        specializations_data = [
            'Heart Specialist',
            'Brain Specialist', 
            'Bone Specialist',
            'Skin Specialist',
            'Child Specialist',
            'General Physician',
            'Cardiologist',
            'Neurologist',
            'Orthopedic Surgeon',
            'Dermatologist',
            'Pediatrician',
            'General Surgeon',
            'Psychiatrist',
            'Gynecologist',
            'Oncologist',
            'Internal Medicine Specialist',
            'Surgical Oncologist',
            'Cardiac Surgeon',
            'Neurosurgeon',
            'Plastic Surgeon',
        ]
        
        for spec_name in specializations_data:
            obj, created = Specialization.objects.get_or_create(
                name=spec_name
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created specialization: {spec_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'✓ Specialization already exists: {spec_name}'))
        
        dept_count = Department.objects.count()
        spec_count = Specialization.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Database seeding completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total Departments: {dept_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total Specializations: {spec_count}'))
