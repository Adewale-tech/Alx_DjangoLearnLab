from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile

def index(request):
    """
    View to render the blog homepage.
    """
    return render(request, 'blog/index.html')

def register(request):
    """
    View to handle user registration using CustomUserCreationForm.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create Profile for new user
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    """
    View to display and update user profile, including User and Profile models.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })