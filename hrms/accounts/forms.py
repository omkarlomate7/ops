from django import forms
from .models import Timesheet, LeaveRequest

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['application_name', 'task_title', 'task_description', 'start_date', 'end_date', 'hours_spent', 'percent_completed', 'total_efforts']


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        