from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def settings_view(request):
    from .forms import SettingsForm

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # preferred_lanaguage not stored; could be saved to profile if created later
            return redirect('settings')
    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})