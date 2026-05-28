from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import User


def role_required(*roles):
    """Restreint l'accès aux rôles listés (ex. @role_required(User.Role.ADMIN))."""

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles and not request.user.is_superuser:
                messages.error(request, "Accès refusé pour votre rôle.")
                return redirect("accounts:dashboard")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def admin_required(view_func):
    """Accès réservé aux administrateurs."""

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect("accounts:dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
