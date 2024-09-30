from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Profile
import logging



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
# @permission_required('accounts.can_view_employee_dashboard', raise_exception=True)
def employee_dashboard(request):
    if request.user.profile.role != 'employee':
        return redirect('unauthorized')
    return render(request, 'accounts/employee_dashboard.html')

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