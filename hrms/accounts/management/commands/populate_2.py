from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import Department, Employee, Timesheet, User

class Command(BaseCommand):
    help = 'Populate the database with fake data for Employees and Timesheets'

    def handle(self, *args, **kwargs):
        fake = Faker('en_IN')

        # Create some sample departments
        departments = ["Engineering", "Sales", "Marketing", "HR", "Finance"]
        for dept_name in departments:
            Department.objects.get_or_create(name=dept_name)

        # Create users and employees
        roles = ['employee', 'team_lead']
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@example.com"
            user = User.objects.create_user(username=username, email=email, password='password123')

            # Create the profile with a random role
            role = random.choice(roles)
            department = Department.objects.order_by('?').first()

            employee = Employee.objects.create(
                user=user,
                department=department,
                job_title=fake.job(),
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                salary=random.uniform(30000, 100000),
                remaining_leaves_month=random.randint(0, 5),
                remaining_leaves_year=random.randint(0, 20),
                team_lead=None,
                salary_slip_url=fake.url(),
                education=random.choice(["Bachelor's", "Master's", "PhD"]),
                address=fake.address(),
                is_active=True,
            )

        # Create some sample timesheets
        for employee in Employee.objects.all():
            for _ in range(random.randint(3, 10)):
                Timesheet.objects.create(
                    employee=employee,
                    application_name=random.choice(['OPS', 'CRM', 'ERP', 'HRMS']),
                    task_title=fake.bs().title(),
                    task_description=fake.text(),
                    start_date=fake.date_between(start_date='-30d', end_date='-15d'),
                    end_date=fake.date_between(start_date='-14d', end_date='today'),
                    hours_spent=random.uniform(1, 8),
                    percent_completed=random.uniform(50.0, 100.0),
                    total_efforts=random.uniform(10, 50),
                    status=random.choice(['Submitted', 'Approved', 'Rejected'])
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with fake data.'))
