from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import Profile, Employee, Timesheet, LeaveRequest
import logging
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .forms import TimesheetForm, LeaveRequestForm
from django.utils import timezone


logger = logging.getLogger(__name__)


def login_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.role == 'employee':
            return redirect('employee_dashboard')
        elif profile.role == 'hr':
            return redirect('hr_dashboard')
        elif profile.role == 'team_lead':
            return redirect('team_lead_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting login for user: {username}")
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            profile = Profile.objects.get(user=user)
            
            # Redirect based on user role
            if profile.role == 'employee':
                return redirect('employee_dashboard')
            elif profile.role == 'hr':
                return redirect('hr_dashboard')
            elif profile.role == 'team_lead':
                return redirect('team_lead_dashboard')
        else:
            print("Failed to authenticate user")
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return redirect('login')

def homepage(request):
    return render(request, 'accounts/homepage.html')


@login_required
def employee_dashboard(request):
    # Check if the user is in the Employee group
    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'accounts/employee_dashboard.html')
    else:
        return redirect('unauthorized')
    
@login_required
def hr_dashboard(request):
    if request.user.profile.role != 'hr':
        return redirect('unauthorized')
    return render(request, 'accounts/hr_dashboard.html')

@login_required
def team_lead_dashboard(request):
    if request.user.profile.role != 'team_lead':
        return redirect('unauthorized')
    return render(request, 'accounts/team_lead_dashboard.html')

def unauthorized(request):
    return render(request, 'accounts/unauthorized.html')

def employee_management(request):
    return render(request, 'employee_management.html')

def recruitment(request):
    return render(request, 'recruitment.html')

def payroll(request):
    # Logic for Payroll page
    return render(request, 'payroll.html')

def employee_list(request):
    query = request.GET.get('search', '')  # Fetch the search term from the query parameters
    if query:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=query) |  # Search by first name
            Q(user__last_name__icontains=query) |   # Search by last name
            Q(user__email__icontains=query)         # Search by email
        )
    else:
        employees = Employee.objects.all()  # Show all employees if no search query

    context = {
        'employees': employees,
    }
    return render(request, 'accounts/emp_list.html', context)

def employee_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'accounts/emp_details.html', {'employee': employee})


@login_required
def submit_timesheet(request):
    if request.method == 'POST':
        row_count = int(request.POST.get('row_count'))  # Get the total number of rows
        
        for i in range(1, row_count + 1):
            application_name = request.POST.get(f'application_name_{i}')
            task_title = request.POST.get(f'task_title_{i}')
            task_description = request.POST.get(f'task_description_{i}')
            start_date = request.POST.get(f'start_date_{i}')
            end_date = request.POST.get(f'end_date_{i}')
            hours_spent = request.POST.get(f'hours_spent_{i}')
            percent_completed = request.POST.get(f'percent_completed_{i}')
            total_efforts = request.POST.get(f'total_efforts_{i}')

            # Check if the row contains valid data, if all fields are not empty
            if all([application_name, task_title, task_description, start_date, end_date, hours_spent, percent_completed, total_efforts]):
                # Save the timesheet only if all fields are valid
                Timesheet.objects.create(
                    user=request.user,
                    application_name=application_name,
                    task_title=task_title,
                    task_description=task_description,
                    start_date=start_date,
                    end_date=end_date,
                    hours_spent=hours_spent,
                    percent_completed=percent_completed,
                    total_efforts=total_efforts
                )
        
        return redirect('timesheet')  # Redirect after submission
    else:
        return render(request, 'accounts/timesheet.html')

# View to display the user's submitted timesheets
@login_required
def my_timesheets(request):
    timesheets = Timesheet.objects.filter(user=request.user)
    return render(request, 'accounts/my_timesheets.html', {
        'timesheets': timesheets
    })

@login_required
def submit_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.submitted_at = timezone.now()
            leave_request.status = 'Pending'
            leave_request.save()
            return redirect('my_leave_requests')
    else:
        form = LeaveRequestForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/submit_leave_request.html', context)

