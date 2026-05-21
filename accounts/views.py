from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserCreateForm


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('accounts:login'))
    else:
        form = UserCreateForm()
    return render(request, 'accounts/register.html', {'form': form})
