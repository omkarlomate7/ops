from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import Profile, Employee, Timesheet, LeaveRequest
import logging
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum, Count
from .forms import TimesheetForm, LeaveRequestForm
from django.utils import timezone
from django.db import IntegrityError

logger = logging.getLogger(__name__)

def login_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.role == 'employee':
            return redirect('emp_land')
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
                return redirect('emp_land')
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
def hr_dashboard(request):
    if request.user.profile.role != 'hr':
        return redirect('unauthorized')
    return render(request, 'accounts/hr_dashboard.html')

@login_required
def team_lead_dashboard(request):
    # Get the logged-in user (team lead)
    user = request.user

    # Fetch pending leave requests from the team lead's team
    leave_requests = LeaveRequest.objects.filter(user__profile__team_lead=user, status='Pending')

    # Get the number of team members reporting to this team lead
    team_members = Profile.objects.filter(team_lead=user)

    context = {
        'leave_requests': leave_requests,
        'team_members': team_members,
    }
    return render(request, 'accounts/team_lead_dashboard.html', context)

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

@login_required
def team_tasks(request):
    # Placeholder view for team tasks
    return render(request, 'accounts/team_tasks.html')

@login_required
def emp_land_view(request):
    # Get the logged-in user (employee)
    user = request.user

    # You can add more employee-specific queries here
    # For now, it's just rendering the template

    return render(request, 'accounts/emp_land.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required
def emp_profile(request):
    try:
        # Fetch the employee profile associated with the logged-in user
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # If the profile does not exist, render an appropriate message
        return render(request, 'accounts/no_profile.html', {
            'message': 'No employee profile exists for the user.'
        })

    # Create the context with employee details
    context = {
        'employees': employee,
    }
    print("Employee details:", context)

    # Render the employee profile page
    return render(request, 'accounts/emp_profile.html', context)

@login_required
def my_details(request):
    try:
        # Check if the Employee profile exists for the logged-in user
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # Redirect or render an error message if no profile exists
        return render(request, 'accounts/no_profile.html', {'message': 'No employee profile exists for the user.'})
    
    context = {
        'employee': {
            'name': employee.user.username,
            'address': employee.address,
            'email': employee.user.email,
            'phone_number': employee.phone_number,
            'joining_date': employee.joining_date,
            'designation': employee.designation,
            'team_lead': employee.profile.team_lead.user.username if employee.profile.team_lead else 'N/A',
            'salary_amount': employee.salary_amount,
            'salary_slip_url': employee.salary_slip_url,
            'remaining_leaves_month': employee.remaining_leaves_month,
            'remaining_leaves_year': employee.remaining_leaves_year,
            'education': employee.education,
            'institution': employee.institution,
            'graduation_year': employee.graduation_year,
            'policies_url': '#',
            'benefits_url': '#',
        }
    }
    return render(request, 'accounts/my_details.html', context)

@login_required
def hr_view_timesheets(request):
    timesheets = Timesheet.objects.select_related('employee', 'employee__user').all()
    return render(request, 'accounts/hr_view_timesheets.html', {'timesheets': timesheets})

from django.shortcuts import get_object_or_404

@login_required
def add_timesheet(request):
    print("add_timesheet view called")
    if request.method == 'POST':
        print("POST request received")
        
        # Printing the entire POST data to see if all fields are being received
        print(f"POST data received: {request.POST}")

        row_count = int(request.POST.get('row_count', 0))  # Get the total number of rows
        print(f"Row count: {row_count}")

        # Iterate through each row and save timesheet entries
        for i in range(1, row_count + 1):
            application_name = request.POST.get(f'application_name_{i}')
            task_title = request.POST.get(f'task_title_{i}')
            task_description = request.POST.get(f'task_description_{i}')
            start_date = request.POST.get(f'start_date_{i}')
            end_date = request.POST.get(f'end_date_{i}')
            hours_spent = request.POST.get(f'hours_spent_{i}')
            percent_completed = request.POST.get(f'percent_completed_{i}')
            total_efforts = request.POST.get(f'total_efforts_{i}')

            # Logging all data retrieved
            print(f"Processing row {i}: application_name={application_name}, task_title={task_title}, "
                  f"task_description={task_description}, start_date={start_date}, end_date={end_date}, "
                  f"hours_spent={hours_spent}, percent_completed={percent_completed}, total_efforts={total_efforts}")

            # Check if the row contains valid data (i.e., all fields are not empty)
            if all([application_name, task_title, task_description, start_date, end_date, hours_spent, percent_completed, total_efforts]):
                try:
                    # Convert numerical data types
                    hours_spent = float(hours_spent)
                    percent_completed = float(percent_completed)
                    total_efforts = float(total_efforts)

                    # Save the timesheet only if all fields are valid
                    print(f"Saving timesheet for row {i}")
                    Timesheet.objects.create(
                        user=request.user,  # Save the timesheet with the logged-in user
                        application_name=application_name,
                        task_title=task_title,
                        task_description=task_description,
                        start_date=start_date,
                        end_date=end_date,
                        hours_spent=hours_spent,
                        percent_completed=percent_completed,
                        total_efforts=total_efforts
                    )

                    print(f"Timesheet saved successfully for row {i}: {timesheet}")
                except ValueError as ve:
                    print(f"Value error for row {i}: {ve}")
                except IntegrityError as ie:
                    print(f"Integrity error for row {i}: {ie}")
                except Exception as e:
                    print(f"Error saving timesheet for row {i}: {e}")
            else:
                print(f"Invalid data for row {i}, skipping save")
        
        messages.success(request, "Timesheet added successfully.")
        return redirect('my_timesheets')  # Redirect after submission, showing user's own timesheets

    # GET method to render the add timesheet form
    print("GET request received, rendering add_timesheet form")
    return render(request, 'accounts/add_timesheet.html')


@login_required
def my_timesheets(request):
    print("my_timesheets view called")
    user_timesheets = Timesheet.objects.filter(user=request.user)
    print(f"Queried timesheets for user {request.user.username}: {user_timesheets.count()} records found.")
    for timesheet in user_timesheets:
        print(f"Timesheet: {timesheet.task_title}, Submitted Date: {timesheet.submit_date}")

    context = {
        'timesheets': user_timesheets
    }
    return render(request, 'accounts/my_timesheets.html', context)

@login_required
def timesheet_dashboard(request):
    # Ensure only HR role can access the dashboard
    if request.user.profile.role != 'hr':
        return redirect('my_timesheets')
    
    # Updated queries to use employee__user instead of user
    total_timesheets = Timesheet.objects.count()
    total_submitted_timesheets = Timesheet.objects.filter(status='Submitted').count()
    total_approved_timesheets = Timesheet.objects.filter(status='Approved').count()
    total_rejected_timesheets = Timesheet.objects.filter(status='Rejected').count()
    
    current_week = timezone.now().isocalendar()[1]
    weekly_submitted_timesheets = Timesheet.objects.filter(submit_date__week=current_week).count()
    weekly_approved_timesheets = Timesheet.objects.filter(submit_date__week=current_week, status='Approved').count()
    weekly_rejected_timesheets = Timesheet.objects.filter(submit_date__week=current_week, status='Rejected').count()

    total_hours_logged = Timesheet.objects.aggregate(total_hours=Sum('hours_spent'))['total_hours'] or 0
    
    # Calculate average hours per staff by grouping by employee__user
    average_hours_per_staff = (
        Timesheet.objects.values('employee__user')
        .annotate(total_hours=Sum('hours_spent'))
        .aggregate(avg_hours=Sum('total_hours') / Count('employee__user'))['avg_hours']
        or 0
    )

    context = {
        'total_submitted_timesheets': total_submitted_timesheets,
        'total_approved_timesheets': total_approved_timesheets,
        'total_rejected_timesheets': total_rejected_timesheets,
        'weekly_submitted_timesheets': weekly_submitted_timesheets,
        'weekly_approved_timesheets': weekly_approved_timesheets,
        'weekly_rejected_timesheets': weekly_rejected_timesheets,
        'total_hours_logged': total_hours_logged,
        'average_hours_per_staff': average_hours_per_staff,
    }
    return render(request, 'accounts/timesheet_dashboard.html', context)

# Updated view function for LeaveRequest
def view_leave_requests(request):
    leave_requests = LeaveRequest.objects.filter(employee__user=request.user)
    return render(request, 'leave_requests.html', {'leave_requests': leave_requests})
