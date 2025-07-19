from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from core.forms import *
from .models import UserProfile
from django.utils import timezone
from datetime import date,timedelta
from django.db.models import Sum
from collections import defaultdict

@login_required
def dashboard_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if user wants to edit profile
    edit_mode = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)

    show_form = not (profile.age and profile.height and profile.weight) or edit_mode

    context = {
        'form': form,
        'profile': profile,
        'show_form': show_form,
        'edit_mode': edit_mode
    }
    return render(request, 'dashboard.html', context)

def home(request):
    return render(request, 'home.html')
 
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})  # ✅ Pass request here

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def meal_planner(request):
    today = timezone.now().date()
    meals = Meal.objects.filter(user=request.user, date=today)

    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('meal_planner')
    else:
        form = MealForm()

    totals = meals.aggregate(
        total_calories=Sum('calories'),
        total_carbs=Sum('carbs'),
        total_protein=Sum('protein'),
        total_fats=Sum('fats'),
    )

    context = {
        'form': form,
        'meals': meals,
        'total_calories': totals['total_calories'] or 0,
        'total_carbs': totals['total_carbs'] or 0,
        'total_protein': totals['total_protein'] or 0,
        'total_fats': totals['total_fats'] or 0,
    }
    return render(request, 'meal_planner.html', context)

@login_required
def meal_history(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date')

    # Group meals by date
    grouped_meals = defaultdict(list)
    for meal in meals:
        grouped_meals[meal.date].append(meal)

    # Convert to list of tuples so it's iterable in templates
    grouped_meals = sorted(grouped_meals.items(), reverse=True)

    return render(request, 'meal_history.html', {
        'grouped_meals': grouped_meals
    })
    

@login_required
def delete_meal(request, pk):
    meal = Meal.objects.get(pk=pk)
    if meal.user == request.user:
        meal.delete()
    return redirect('meal_planner')

@login_required
def water(request):
    user = request.user
    today = date.today()

    # Get or create the goal
    goal_obj, created = WaterGoal.objects.get_or_create(user=user)
    goal_form = WaterGoalForm(instance=goal_obj)

    # Get today’s total intake
    total_intake = WaterIntake.objects.filter(user=user, date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    progress = int((total_intake / goal_obj.daily_goal) * 100) if goal_obj.daily_goal else 0

    # Handle form submission
    if request.method == 'POST':
        if 'daily_goal' in request.POST:
            # Goal form submission
            goal_form = WaterGoalForm(request.POST, instance=goal_obj)
            if goal_form.is_valid():
                goal_form.save()
                return redirect('water')
        else:
            # Water intake submission
            intake_form = WaterIntakeForm(request.POST)
            if intake_form.is_valid():
                intake = intake_form.save(commit=False)
                intake.user = user
                intake.save()
                return redirect('water')
    else:
        intake_form = WaterIntakeForm()

    context = {
        'goal': goal_obj,
        'goal_form': goal_form,
        'form': intake_form,
        'total_intake': total_intake,
        'progress': progress,
    }

    return render(request, 'water.html', context)
@login_required
def workout_view(request):
    workouts = Workout.objects.all()
    log_form = WorkoutLogForm()

    if request.method == 'POST' and 'log_progress' in request.POST:
        log_form = WorkoutLogForm(request.POST)
        if log_form.is_valid():
            log = log_form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('workout')  # redirect back to same page

    return render(request, 'workout.html', {
        'workouts': workouts,
        'log_form': log_form,
    })
@login_required
def bmi(request):
    bmi = result = None

    if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height'] / 100  # convert to meters
            weight = form.cleaned_data['weight']
            bmi = weight / (height ** 2)
            if bmi < 18.5:
                result = "Underweight"
            elif 18.5 <= bmi < 24.9:
                result = "Normal"
            elif 25 <= bmi < 29.9:
                result = "Overweight"
            else:
                result = "Obese"

            # Save if needed

    else:
        form = BMICalculatorForm()

    return render(request, 'bmi.html', {
        'form': form,
        'bmi': round(bmi, 2) if bmi else None,
        'result': result
    })

