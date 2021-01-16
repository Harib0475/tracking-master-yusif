from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main_app.models import Post, Device
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Updated Successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        user = request.user.id

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': Post.objects.all(),
        'devices': Device.objects.filter(device_user=user),
        'total_devices': Device.objects.count(),
        'total_posts': Post.objects.count(),
    }
    return render(request, 'user/profile.html', context)
