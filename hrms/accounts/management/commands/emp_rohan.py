from faker import Faker
from django.contrib.auth.models import User
from accounts.models import Employee, Profile, Department

# Initialize Faker
fake = Faker()

# Create a user
username = 'mira'
password = 'Pass@12345'
first_name = 'mira'
last_name = 'patil'
email = fake.email()

# Check if the user exists
if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(username=username, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()

    # Create a department if needed
    department, created = Department.objects.get_or_create(name=fake.company())

    # Create Employee profile
    employee = Employee.objects.create(
        user=user,
        department=department,
        job_title=fake.job(),
        hire_date=fake.date_this_decade(),
        salary=fake.random_number(digits=5),
        is_active=True
    )

    # Create Profile
    Profile.objects.create(
        user=user,
        role='employee',
        team_lead=None  # Update with team lead if applicable
    )

    print(f"Employee profile for {first_name} {last_name} created successfully!")
else:
    print(f"User with username {username} already exists.")
