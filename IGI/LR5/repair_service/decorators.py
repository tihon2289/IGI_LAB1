from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Декоратор: доступ только для администраторов (is_staff или role='admin')"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему')
            return redirect('login')
        
        is_admin = request.user.is_staff or (
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'admin'
        )
        
        if not is_admin:
            messages.error(request, 'У вас нет прав доступа к этой странице')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper