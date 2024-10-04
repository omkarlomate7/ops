from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    job_title = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_leaves_month = models.IntegerField(default=0)  # Remaining leaves for current month
    remaining_leaves_year = models.IntegerField(default=0)   # Remaining leaves for current year
    team_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="team_lead")
    salary_slip_url = models.URLField(max_length=255, blank=True)  # URL to download salary slip
    education = models.CharField(max_length=255, blank=True)  # Employee education information
    address = models.TextField(blank=True)  # Employee's address
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.job_title}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('team_lead', 'Team Lead'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        permissions = [
            ("can_view_hr_dashboard", "Can view HR dashboard"),
            ("can_view_employee_dashboard", "Can view Employee dashboard"),
            ("can_view_team_lead_dashboard", "Can view Team Lead dashboard"),
        ]

class Timesheet(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application_name = models.CharField(max_length=255)
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)
    percent_completed = models.DecimalField(max_digits=5, decimal_places=2)
    total_efforts = models.DecimalField(max_digits=5, decimal_places=2)
    submit_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Submitted')

    def __str__(self):
        return f"{self.user.username} - {self.task_title}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    hr_approval = models.BooleanField(default=False)
    team_lead_approval = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

    def is_approved(self):
        return self.hr_approval and self.team_lead_approval