from django.core.management.base import BaseCommand
from apps.doctors.models import Department, Specialization


class Command(BaseCommand):
    help = 'Seed the database with sample departments and specializations'

    def handle(self, *args, **options):
        # Create Departments
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular disease treatment'},
            {'name': 'Neurology', 'description': 'Brain and nervous system disorders'},
            {'name': 'Orthopedics', 'description': 'Bone, joint and muscle disorders'},
            {'name': 'Pediatrics', 'description': 'Child health and medical care'},
            {'name': 'Obstetrics & Gynecology', 'description': 'Pregnancy, childbirth and women health'},
            {'name': 'Dermatology', 'description': 'Skin, hair and nail disorders'},
            {'name': 'Oncology', 'description': 'Cancer treatment and management'},
            {'name': 'Psychiatry', 'description': 'Mental health and behavioral disorders'},
            {'name': 'General Medicine', 'description': 'General medical conditions and treatments'},
            {'name': 'Surgery', 'description': 'Surgical procedures and operations'},
        ]

        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {dept.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Department already exists: {dept.name}'))

        # Create Specializations
        specializations_data = [
            'Cardiology',
            'Interventional Cardiology',
            'Cardiac Surgery',
            'Neurosurgery',
            'Clinical Neurology',
            'Orthopedic Surgery',
            'Sports Medicine',
            'Pediatric Medicine',
            'Neonatology',
            'Obstetrics',
            'Gynecology',
            'Dermatology',
            'Medical Oncology',
            'Surgical Oncology',
            'Psychiatry',
            'Clinical Psychology',
            'Internal Medicine',
            'General Surgery',
            'Gastrointestinal Surgery',
            'Trauma Surgery',
        ]

        for spec_name in specializations_data:
            spec, created = Specialization.objects.get_or_create(name=spec_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created specialization: {spec.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Specialization already exists: {spec.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded departments and specializations!'))
