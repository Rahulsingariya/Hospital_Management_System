from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a default superuser for initial setup'

    def handle(self, *args, **options):
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists. Skipping creation.'))
            return

        # Create superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@hospital.com',
            password='admin123456',
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created superuser:')
        )
        self.stdout.write(f'  Username: admin')
        self.stdout.write(f'  Password: admin123456')
        self.stdout.write(f'  Email: admin@hospital.com')
        self.stdout.write(
            self.style.WARNING('\n⚠️  IMPORTANT: Change this password immediately after logging in!')
        )
