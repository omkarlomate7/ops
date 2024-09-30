from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/'):
            if not request.user.is_authenticated:
                return redirect('login')
            role = request.user.profile.role
            if 'employee' in request.path and role != 'employee':
                return redirect('unauthorized')
            elif 'hr' in request.path and role != 'hr':
                return redirect('unauthorized')
            elif 'team_lead' in request.path and role != 'team_lead':
                return redirect('unauthorized')
        response = self.get_response(request)
        return response
