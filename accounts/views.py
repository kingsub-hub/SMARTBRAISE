from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .decorators import admin_required
from .forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileForm,
    ProfileUserForm,
    RegistrationForm,
    UserEditForm,
)
from .models import LoginHistory, Profile, User


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _user_agent(request):
    return (request.META.get("HTTP_USER_AGENT") or "")[:500]


def _log_login(request, user=None, *, success):
    LoginHistory.objects.create(
        user=user if user and user.pk else None,
        ip_address=_client_ip(request),
        user_agent=_user_agent(request),
        success=success,
    )


def _safe_next_url(request, url):
    if url and url_has_allowed_host_and_scheme(
        url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return url
    return ""


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        _log_login(request, user=user, success=True)
        messages.success(request, "Compte créé. Bienvenue !")
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    next_url = _safe_next_url(
        request, request.POST.get("next") or request.GET.get("next", "")
    )
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        if form.cleaned_data.get("remember_me"):
            request.session.set_expiry(60 * 60 * 24 * 14)  # 14 jours
        else:
            request.session.set_expiry(0)  # expire à la fermeture du navigateur
        _log_login(request, user=user, success=True)
        return redirect(next_url or "accounts:dashboard")
    if request.method == "POST":
        email = request.POST.get("username", "").strip().lower()
        user = User.objects.filter(email__iexact=email).first() if email else None
        _log_login(request, user=user, success=False)
    return render(
        request, "accounts/login.html", {"form": form, "next": next_url}
    )


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.method == "POST":
        logout(request)
        request.session.flush()
        messages.info(request, "Vous êtes déconnecté.")
        return redirect("accounts:login")
    return render(request, "accounts/logout.html")


@login_required
def dashboard_view(request):
    recent_logins = request.user.login_history.all()[:10]
    return render(
        request,
        "accounts/dashboard.html",
        {"recent_logins": recent_logins},
    )


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_form = ProfileUserForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Profil mis à jour.")
        return redirect("accounts:profile")
    return render(
        request,
        "accounts/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def password_change_view(request):
    form = CustomPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Mot de passe modifié.")
        return redirect("accounts:profile")
    return render(request, "accounts/password_change.html", {"form": form})


@admin_required
def manage_users_view(request):
    users = User.objects.all().order_by("-date_joined")
    search = request.GET.get("q", "").strip()
    current_role = request.GET.get("role", "")
    current_status = request.GET.get("status", "")

    if search:
        users = users.filter(
            Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )
    if current_role:
        users = users.filter(role=current_role)
    if current_status == "active":
        users = users.filter(is_active=True)
    elif current_status == "inactive":
        users = users.filter(is_active=False)

    return render(
        request,
        "accounts/manage_users.html",
        {
            "users": users,
            "search": search,
            "current_role": current_role,
            "current_status": current_status,
            "roles": User.Role.choices,
        },
    )


@admin_required
def user_edit_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=target_user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Utilisateur mis à jour.")
        return redirect("accounts:manage_users")
    return render(
        request,
        "accounts/user_edit.html",
        {"form": form, "target_user": target_user},
    )


@admin_required
@require_http_methods(["POST"])
def user_toggle_active_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save(update_fields=["is_active"])
        messages.success(request, "Statut mis à jour.")
    return redirect("accounts:manage_users")
