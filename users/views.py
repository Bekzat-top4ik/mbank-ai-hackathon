from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from goals.models import Goal


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    total_goals = goals.count()
    completed_goals = goals.filter(is_completed=True).count()
    total_saved = sum(g.current_amount for g in goals)
    completed_goals_list = goals.filter(is_completed=True)

    # Значки
    badges = []
    if total_goals >= 1:
        badges.append('🎯 Первая цель')
    if total_goals >= 3:
        badges.append('🔥 Целеустремлённый')
    if completed_goals >= 1:
        badges.append('✅ Выполнил цель')
    if total_saved >= 10000:
        badges.append('💰 Накопил 10,000 сом')
    if total_saved >= 100000:
        badges.append('🏆 Накопил 100,000 сом')

    # Мотивационная фраза
    if total_goals == 0:
        motivation = 'Поставь первую цель и начни путь к мечте! 🚀'
    elif completed_goals > 0:
        motivation = 'Ты уже выполнил цель! Продолжай в том же духе! 🏆'
    elif total_saved > 0:
        motivation = 'Ты на правильном пути! Каждый сом приближает тебя к цели! 💪'
    else:
        motivation = 'Начни пополнять свои цели — первый шаг самый важный! 🌟'
    if request.method == 'POST':
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        if email:
            request.user.email = email
            request.user.save()
        if avatar:
            profile.avatar = avatar
            profile.save()
        return redirect('profile')
    context = {
        'profile': profile,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'total_saved': total_saved,
        'badges': badges,
        'motivation': motivation,
        'completed_goals_list': completed_goals_list,
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'users/delete_account.html')