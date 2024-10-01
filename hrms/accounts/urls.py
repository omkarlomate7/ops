from django.urls import path
from . import views
from .views import employee_list

urlpatterns = [
    path('', views.home, name='home'),  # Root URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/hr/', views.hr_dashboard, name='hr_dashboard'),
    path('dashboard/team_lead/', views.team_lead_dashboard, name='team_lead_dashboard'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('employee_management/', views.employee_management, name='employee_management'),
    path('recruitment/', views.recruitment, name='recruitment'),
    path('payroll/', views.payroll, name='payroll'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('employees/', employee_list, name='employee_list'),
    path('timesheet/', views.submit_timesheet, name='timesheet'),
    path('my_timesheets/', views.my_timesheets, name='my_timesheets'),
    
]
