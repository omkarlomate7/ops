from django.db import models
from django.contrib.auth.models import User

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
