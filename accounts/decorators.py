from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import Profile


def teacher_required(view_func):
    """Decorator to restrict view to teachers only."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.profile.is_teacher():
                return view_func(request, *args, **kwargs)
        except Profile.DoesNotExist:
            pass
        return HttpResponseForbidden("You must be a teacher to access this page.")
    return wrapper


def student_required(view_func):
    """Decorator to restrict view to students only."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.profile.is_student():
                return view_func(request, *args, **kwargs)
        except Profile.DoesNotExist:
            pass
        return HttpResponseForbidden("You must be a student to access this page.")
    return wrapper
