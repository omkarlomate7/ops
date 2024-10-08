# Generated by Django 5.1.1 on 2024-10-04 10:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("job_title", models.CharField(max_length=100)),
                ("hire_date", models.DateField()),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("remaining_leaves_month", models.IntegerField(default=0)),
                ("remaining_leaves_year", models.IntegerField(default=0)),
                ("salary_slip_url", models.URLField(blank=True, max_length=255)),
                ("education", models.CharField(blank=True, max_length=255)),
                ("address", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "department",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="employees",
                        to="accounts.department",
                    ),
                ),
                (
                    "team_lead",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="team_lead",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LeaveRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("reason", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                ("hr_approval", models.BooleanField(default=False)),
                ("team_lead_approval", models.BooleanField(default=False)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "employee",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leave_requests",
                        to="accounts.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("employee", "Employee"),
                            ("hr", "HR"),
                            ("team_lead", "Team Lead"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_view_hr_dashboard", "Can view HR dashboard"),
                    ("can_view_employee_dashboard", "Can view Employee dashboard"),
                    ("can_view_team_lead_dashboard", "Can view Team Lead dashboard"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Timesheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("application_name", models.CharField(max_length=255)),
                ("task_title", models.CharField(max_length=255)),
                ("task_description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("hours_spent", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "percent_completed",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("total_efforts", models.DecimalField(decimal_places=2, max_digits=5)),
                ("submit_date", models.DateField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Submitted", "Submitted"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Submitted",
                        max_length=10,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="timesheets",
                        to="accounts.employee",
                    ),
                ),
            ],
        ),
    ]
