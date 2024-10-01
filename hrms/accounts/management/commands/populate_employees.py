import os
import django
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from accounts.models import Employee, Department
import random

class Command(BaseCommand):
    help = 'Populate the database with fake Indian employee data'

    def handle(self, *args, **kwargs):
        # Ensure Django is properly configured
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
        django.setup()

        fake = Faker('en_IN')  # Setting the locale for India
        departments = ['HR', 'Engineering', 'Marketing', 'Sales', 'Finance', 'Operations']

        # Create departments if they don't exist
        for dept_name in departments:
            Department.objects.get_or_create(name=dept_name)

        # Generate fake employees
        for _ in range(50):  # Number of fake employees to generate
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.unique.user_name()
            email = fake.email()
            department = Department.objects.order_by("?").first()  # Randomly assign a department
            job_title = random.choice(['Software Engineer', 'Data Analyst', 'HR Manager', 'Sales Executive'])
            hire_date = fake.date_this_decade()
            salary = round(random.uniform(20000, 100000), 2)
            
            # Create a new user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password='password123'  # You can customize this if needed
            )

            # Create the employee profile
            Employee.objects.create(
                user=user,
                department=department,
                job_title=job_title,
                hire_date=hire_date,
                salary=salary,
                is_active=True
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake employee data'))
