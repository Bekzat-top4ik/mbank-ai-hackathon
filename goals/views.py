from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Goal
from .forms import GoalForm

@login_required
def goals_list(request):
    goals = Goal.objects.filter(user=request.user).order_by('created_at')
    total_target = sum(g.target_amount for g in goals)
    total_current = sum(g.current_amount for g in goals)
    today = date.today()
    warnings = []
    for goal in goals:
        days_left = (goal.deadline - today).days
        if days_left < 0:
            warnings.append(f'⛔ Дедлайн "{goal.title}" уже прошёл!')
        elif days_left <= 7:
            warnings.append(f'⚠️ До дедлайна "{goal.title}" осталось {days_left} дней!')
    return render(request, 'goals/goals_list.html', {
        'goals': goals,
        'total_target': total_target,
        'total_current': total_current,
        'warnings': warnings,
    })

@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals_list')
    else:
        form = GoalForm()
    return render(request, 'goals/add_goal.html', {'form': form})

@login_required
def edit_goal(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/edit_goal.html', {'form': form, 'goal': goal})

@login_required
def delete_goal(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    goal.delete()
    return redirect('goals_list')

@login_required
def add_amount(request, id):
    goal = get_object_or_404(Goal, id=id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            goal.current_amount += int(amount)
            goal.save()
            if goal.percentage() >= 100:
                goal.is_completed = True
                goal.save()

    return redirect('goals_list')