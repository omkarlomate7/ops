from django.urls import path
from . import views
from .views import employee_list, emp_profile

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),  # Root URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard URLs
    path('dashboard/emp_land/', views.emp_land_view, name='emp_land'),
    path('dashboard/hr/', views.hr_dashboard, name='hr_dashboard'),
    path('dashboard/team_lead/', views.team_lead_dashboard, name='team_lead_dashboard'),

    # Authorization-related URL
    path('unauthorized/', views.unauthorized, name='unauthorized'),

    # Employee Management URLs
    path('employee_management/', views.employee_management, name='employee_management'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_details, name='employee_details'),

    # Recruitment and Payroll URLs
    path('recruitment/', views.recruitment, name='recruitment'),
    path('payroll/', views.payroll, name='payroll'),

    # Timesheet Functionality URLs
    path('timesheet/add/', views.add_timesheet, name='add_timesheet'),  # URL for adding a new timesheet
    path('timesheet_dashboard/', views.timesheet_dashboard, name='timesheet_dashboard'),  # Main timesheet dashboard
    path('timesheets/view/', views.hr_view_timesheets, name='hr_view_timesheets'),  # HR-specific view for all employees' timesheets
    path('my_timesheets/', views.my_timesheets, name='my_timesheets'),  # Employee's personal timesheet view

    # Leave Request URLs
    path('submit_leave_request/', views.submit_leave_request, name='submit_leave_request'),  # URL to submit leave request
    path('my_leave_requests/', views.my_details, name='my_leave_requests'),  # URL to view submitted leave requests

    # Employee Profile URLs
    path('profile/', views.my_details, name='my_details'),
    path('profile/view/', views.emp_profile, name='emp_profile'),
]