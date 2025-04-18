from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta, date
from .models import (
    UserProfile, DietPreference, Allergen, Cuisine, Ingredient,
    Meal, DietPlan, DietPlanMeal, WeightLog, MealLog
)
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, DietPreferenceForm,
    WeightLogForm, MealLogForm, BMRCalculatorForm, MealSearchForm, ContactForm
)

# Home Page View
def home(request):
    return render(request, 'core/home.html')

# About Page View
def about(request):
    return render(request, 'core/about.html')

# Contact Page View
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send email)
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

# User Registration View
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}. Please complete your profile.')
            return redirect('profile_setup')
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})

# Profile Setup View
@login_required
def profile_setup(request):
    user_profile = request.user.profile

    if user_profile.profile_completed:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.update_daily_calories()
            profile.profile_completed = True
            profile.save()

            # Create default diet preference
            DietPreference.objects.get_or_create(user=request.user)

            messages.success(request, 'Your profile has been set up successfully!')
            return redirect('diet_preferences')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'core/profile_setup.html', {'form': form})

# Diet Preferences View
@login_required
def diet_preferences(request):
    try:
        diet_pref = DietPreference.objects.get(user=request.user)
    except DietPreference.DoesNotExist:
        diet_pref = DietPreference(user=request.user)
        diet_pref.save()

    if request.method == 'POST':
        form = DietPreferenceForm(request.POST, instance=diet_pref)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your diet preferences have been updated successfully!')

            # Check if this is the first time setting up preferences
            if not request.user.profile.profile_completed:
                request.user.profile.profile_completed = True
                request.user.profile.save()
                return redirect('dashboard')
            else:
                return redirect('dashboard')
    else:
        form = DietPreferenceForm(instance=diet_pref)

    return render(request, 'core/diet_preferences.html', {'form': form})

# User Profile View
@login_required
def profile(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.update_daily_calories()
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Get weight logs for chart
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('date')[:10]

    context = {
        'form': form,
        'weight_logs': weight_logs,
        'bmr': user_profile.calculate_bmr(),
        'tdee': user_profile.calculate_tdee(),
        'daily_calories': user_profile.daily_calories,
    }

    return render(request, 'core/profile.html', context)

# Dashboard View
@login_required
def dashboard(request):
    user_profile = request.user.profile

    # If profile not completed, redirect to profile setup
    if not user_profile.profile_completed:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    # Get active diet plan
    active_plan = DietPlan.objects.filter(user=request.user, is_active=True).first()

    # Get today's meals from the active plan
    today_meals = []
    if active_plan:
        today_weekday = timezone.now().weekday() + 1  # 1-7 for Monday-Sunday
        today_meals = DietPlanMeal.objects.filter(diet_plan=active_plan, day=today_weekday)

    # Get today's meal logs
    today = timezone.now().date()
    meal_logs = MealLog.objects.filter(user=request.user, date=today)

    # Calculate calories consumed today
    calories_consumed = meal_logs.aggregate(Sum('calories'))['calories__sum'] or 0
    calories_remaining = user_profile.daily_calories - calories_consumed if user_profile.daily_calories else 0

    # Get recent weight logs
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'user_profile': user_profile,
        'active_plan': active_plan,
        'today_meals': today_meals,
        'meal_logs': meal_logs,
        'calories_consumed': calories_consumed,
        'calories_remaining': calories_remaining,
        'weight_logs': weight_logs,
    }

    return render(request, 'core/dashboard.html', context)

# Calorie Calculator View
def calorie_calculator(request):
    result = None

    if request.method == 'POST':
        form = BMRCalculatorForm(request.POST)
        if form.is_valid():
            bmr = form.calculate_bmr()
            tdee = form.calculate_tdee()
            daily_calories = form.calculate_daily_calories()

            result = {
                'bmr': int(bmr),
                'tdee': tdee,
                'daily_calories': daily_calories,
                'goal': dict(UserProfile.GOAL_CHOICES)[form.cleaned_data['goal']],
            }
    else:
        # Pre-fill form with user data if logged in
        initial_data = {}
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            profile = request.user.profile
            if profile.age and profile.gender and profile.height and profile.weight:
                initial_data = {
                    'age': profile.age,
                    'gender': profile.gender,
                    'height': profile.height,
                    'weight': profile.weight,
                    'activity_level': profile.activity_level,
                    'goal': profile.goal,
                }
        form = BMRCalculatorForm(initial=initial_data)

    return render(request, 'core/calorie_calculator.html', {'form': form, 'result': result})

# Meal Library View
def meal_library(request):
    meals = Meal.objects.all()

    # Apply filters from search form
    form = MealSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        meal_type = form.cleaned_data.get('meal_type')
        min_calories = form.cleaned_data.get('min_calories')
        max_calories = form.cleaned_data.get('max_calories')
        is_vegetarian = form.cleaned_data.get('is_vegetarian')
        is_vegan = form.cleaned_data.get('is_vegan')
        is_gluten_free = form.cleaned_data.get('is_gluten_free')
        cuisine = form.cleaned_data.get('cuisine')

        if query:
            meals = meals.filter(name__icontains=query)

        if meal_type:
            meals = meals.filter(meal_type=meal_type)

        if min_calories is not None:
            meals = meals.filter(calories__gte=min_calories)

        if max_calories is not None:
            meals = meals.filter(calories__lte=max_calories)

        if is_vegetarian:
            meals = meals.filter(is_vegetarian=True)

        if is_vegan:
            meals = meals.filter(is_vegan=True)

        if is_gluten_free:
            meals = meals.filter(is_gluten_free=True)

        if cuisine:
            meals = meals.filter(cuisines=cuisine)

    # Get user's diet preferences if logged in
    user_diet_type = None
    if request.user.is_authenticated:
        try:
            diet_pref = DietPreference.objects.get(user=request.user)
            user_diet_type = diet_pref.diet_type
        except DietPreference.DoesNotExist:
            pass

    context = {
        'meals': meals,
        'form': form,
        'user_diet_type': user_diet_type,
    }

    return render(request, 'core/meal_library.html', context)

# Meal Detail View
def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    ingredients = meal.mealingredient_set.all()

    # Check if meal matches user's diet preferences
    diet_match = True
    diet_mismatch_reason = None

    if request.user.is_authenticated:
        try:
            diet_pref = DietPreference.objects.get(user=request.user)

            # Check diet type compatibility
            if diet_pref.diet_type == 'V' and not meal.is_vegetarian:
                diet_match = False
                diet_mismatch_reason = "This meal is not vegetarian."
            elif diet_pref.diet_type == 'VG' and not meal.is_vegan:
                diet_match = False
                diet_mismatch_reason = "This meal is not vegan."

            # Check for allergies
            user_allergies = diet_pref.allergies.all()
            for ingredient in ingredients:
                for allergy in user_allergies:
                    if allergy.name.lower() in ingredient.ingredient.name.lower():
                        diet_match = False
                        diet_mismatch_reason = f"This meal contains {ingredient.ingredient.name}, which you may be allergic to."
                        break
        except DietPreference.DoesNotExist:
            pass

    context = {
        'meal': meal,
        'ingredients': ingredients,
        'diet_match': diet_match,
        'diet_mismatch_reason': diet_mismatch_reason,
    }

    return render(request, 'core/meal_detail.html', context)

# Weight Log View
@login_required
def weight_log(request):
    logs = WeightLog.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            weight_log = form.save(commit=False)
            weight_log.user = request.user

            # Check if a log already exists for this date
            existing_log = WeightLog.objects.filter(user=request.user, date=weight_log.date).first()
            if existing_log:
                existing_log.weight = weight_log.weight
                existing_log.notes = weight_log.notes
                existing_log.save()
                messages.success(request, 'Weight log updated successfully!')
            else:
                weight_log.save()
                messages.success(request, 'Weight log added successfully!')

            # Update user profile weight
            profile = request.user.profile
            profile.weight = weight_log.weight
            profile.update_daily_calories()
            profile.save()

            return redirect('weight_log')
    else:
        # Pre-fill with today's date and current weight
        initial_data = {
            'date': date.today(),
            'weight': request.user.profile.weight
        }
        form = WeightLogForm(initial=initial_data)

    context = {
        'form': form,
        'logs': logs,
    }

    return render(request, 'core/weight_log.html', context)

# Meal Log View
@login_required
def meal_log(request):
    # Get date from query parameters or use today
    log_date_str = request.GET.get('date')
    try:
        log_date = timezone.datetime.strptime(log_date_str, '%Y-%m-%d').date() if log_date_str else timezone.now().date()
    except ValueError:
        log_date = timezone.now().date()

    # Get logs for the selected date
    logs = MealLog.objects.filter(user=request.user, date=log_date).order_by('time')

    # Calculate total calories and macros for the day
    daily_totals = logs.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fat=Sum('fat')
    )

    # Check if a meal_id was provided in the query parameters
    meal_id = request.GET.get('meal_id')
    initial_data = {
        'date': log_date,
        'time': timezone.now().time().strftime('%H:%M')
    }

    if meal_id:
        try:
            meal = Meal.objects.get(id=meal_id)
            initial_data['meal'] = meal
            initial_data['meal_type'] = meal.meal_type
        except Meal.DoesNotExist:
            pass

    if request.method == 'POST':
        form = MealLogForm(request.POST)
        if form.is_valid():
            meal_log = form.save(commit=False)
            meal_log.user = request.user

            # If a meal was selected, use its nutritional info
            if meal_log.meal:
                meal = meal_log.meal
                meal_log.calories = meal.calories
                meal_log.protein = meal.protein
                meal_log.carbs = meal.carbs
                meal_log.fat = meal.fat

            meal_log.save()
            messages.success(request, 'Meal log added successfully!')
            return redirect(f'meal_log?date={meal_log.date}')
    else:
        # Pre-fill with current date and time and meal if provided
        form = MealLogForm(initial=initial_data)

    # Get date navigation links
    prev_date = log_date - timedelta(days=1)
    next_date = log_date + timedelta(days=1)

    context = {
        'form': form,
        'logs': logs,
        'log_date': log_date,
        'prev_date': prev_date,
        'next_date': next_date,
        'daily_totals': daily_totals,
        'daily_target': request.user.profile.daily_calories,
    }

    return render(request, 'core/meal_log.html', context)

# Generate Diet Plan View
@login_required
def generate_diet_plan(request):
    user_profile = request.user.profile

    # If profile not completed, redirect to profile setup
    if not user_profile.profile_completed:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    if request.method == 'POST':
        # Process diet plan generation
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            messages.error(request, 'Please select start and end dates.')
            return redirect('generate_diet_plan')

        # Create a new diet plan
        diet_plan = DietPlan(
            user=request.user,
            name=f"Diet Plan {start_date} to {end_date}",
            start_date=start_date,
            end_date=end_date,
            total_calories=user_profile.daily_calories,
            is_active=True
        )
        diet_plan.save()

        # Set all other plans to inactive
        DietPlan.objects.filter(user=request.user).exclude(id=diet_plan.id).update(is_active=False)

        # Generate meals for the plan (simplified example)
        # In a real app, this would use more sophisticated logic based on user preferences
        try:
            diet_pref = DietPreference.objects.get(user=request.user)

            # Filter meals based on diet preferences
            breakfast_meals = Meal.objects.filter(meal_type='B')
            lunch_meals = Meal.objects.filter(meal_type='L')
            dinner_meals = Meal.objects.filter(meal_type='D')
            snack_meals = Meal.objects.filter(meal_type='S')

            # Apply diet type filter
            if diet_pref.diet_type == 'V':  # Vegetarian
                breakfast_meals = breakfast_meals.filter(is_vegetarian=True)
                lunch_meals = lunch_meals.filter(is_vegetarian=True)
                dinner_meals = dinner_meals.filter(is_vegetarian=True)
                snack_meals = snack_meals.filter(is_vegetarian=True)
            elif diet_pref.diet_type == 'VG':  # Vegan
                breakfast_meals = breakfast_meals.filter(is_vegan=True)
                lunch_meals = lunch_meals.filter(is_vegan=True)
                dinner_meals = dinner_meals.filter(is_vegan=True)
                snack_meals = snack_meals.filter(is_vegan=True)

            # Get preferred cuisines
            preferred_cuisines = diet_pref.preferred_cuisines.all()
            if preferred_cuisines.exists():
                breakfast_meals = breakfast_meals.filter(cuisines__in=preferred_cuisines).distinct()
                lunch_meals = lunch_meals.filter(cuisines__in=preferred_cuisines).distinct()
                dinner_meals = dinner_meals.filter(cuisines__in=preferred_cuisines).distinct()
                snack_meals = snack_meals.filter(cuisines__in=preferred_cuisines).distinct()

            # Exclude disliked ingredients
            disliked_ingredients = diet_pref.disliked_ingredients.all()
            if disliked_ingredients.exists():
                for ingredient in disliked_ingredients:
                    breakfast_meals = breakfast_meals.exclude(ingredients=ingredient)
                    lunch_meals = lunch_meals.exclude(ingredients=ingredient)
                    dinner_meals = dinner_meals.exclude(ingredients=ingredient)
                    snack_meals = snack_meals.exclude(ingredients=ingredient)

            # Create meal plan for each day (simplified)
            for day in range(1, 8):  # 1-7 for Monday-Sunday
                # Get random meals for each meal type
                breakfast = breakfast_meals.order_by('?').first() if breakfast_meals.exists() else None
                lunch = lunch_meals.order_by('?').first() if lunch_meals.exists() else None
                dinner = dinner_meals.order_by('?').first() if dinner_meals.exists() else None
                snack = snack_meals.order_by('?').first() if snack_meals.exists() else None

                # Add meals to the plan
                if breakfast:
                    DietPlanMeal.objects.create(diet_plan=diet_plan, meal=breakfast, day=day, meal_type='B')
                if lunch:
                    DietPlanMeal.objects.create(diet_plan=diet_plan, meal=lunch, day=day, meal_type='L')
                if dinner:
                    DietPlanMeal.objects.create(diet_plan=diet_plan, meal=dinner, day=day, meal_type='D')
                if snack:
                    DietPlanMeal.objects.create(diet_plan=diet_plan, meal=snack, day=day, meal_type='S')

            messages.success(request, 'Diet plan generated successfully!')
            return redirect('view_diet_plan', plan_id=diet_plan.id)

        except Exception as e:
            messages.error(request, f'Error generating diet plan: {str(e)}')
            diet_plan.delete()  # Clean up the partially created plan
            return redirect('generate_diet_plan')

    # Get user's diet preferences
    try:
        diet_pref = DietPreference.objects.get(user=request.user)
    except DietPreference.DoesNotExist:
        diet_pref = None

    context = {
        'user_profile': user_profile,
        'diet_pref': diet_pref,
        'today': date.today().strftime('%Y-%m-%d'),
        'week_later': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
    }

    return render(request, 'core/generate_diet_plan.html', context)

# View Diet Plan
@login_required
def view_diet_plan(request, plan_id):
    diet_plan = get_object_or_404(DietPlan, id=plan_id, user=request.user)

    # Get meals grouped by day
    days = {}
    for day_num in range(1, 8):  # 1-7 for Monday-Sunday
        day_name = dict(DietPlanMeal.DAY_CHOICES)[day_num]
        days[day_num] = {
            'name': day_name,
            'meals': DietPlanMeal.objects.filter(diet_plan=diet_plan, day=day_num).order_by('meal_type')
        }

    # Calculate daily calories and macros
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    meal_count = 0

    for day_meals in days.values():
        for meal_plan in day_meals['meals']:
            total_calories += meal_plan.meal.calories
            total_protein += float(meal_plan.meal.protein)
            total_carbs += float(meal_plan.meal.carbs)
            total_fat += float(meal_plan.meal.fat)
            meal_count += 1

    # Calculate daily averages
    daily_calories = 0
    daily_protein = 0
    daily_carbs = 0
    daily_fat = 0

    # If we have meals in the plan, calculate the averages
    if meal_count > 0:
        # Get the number of days with meals
        days_with_meals = len([day for day, data in days.items() if data['meals'].exists()])

        if days_with_meals > 0:
            daily_calories = total_calories // days_with_meals
            daily_protein = round(total_protein / days_with_meals, 1)
            daily_carbs = round(total_carbs / days_with_meals, 1)
            daily_fat = round(total_fat / days_with_meals, 1)

            # Update the diet plan with the calculated totals if they're not already set
            if diet_plan.total_calories == 0 or diet_plan.total_protein == 0:
                diet_plan.total_calories = daily_calories
                diet_plan.total_protein = daily_protein
                diet_plan.total_carbs = daily_carbs
                diet_plan.total_fat = daily_fat
                diet_plan.save()
    else:
        # If there are no meals in the plan, use the values stored in the diet plan
        daily_calories = diet_plan.total_calories
        daily_protein = diet_plan.total_protein
        daily_carbs = diet_plan.total_carbs
        daily_fat = diet_plan.total_fat

    context = {
        'diet_plan': diet_plan,
        'days': days,
        'daily_calories': daily_calories,
        'daily_protein': daily_protein,
        'daily_carbs': daily_carbs,
        'daily_fat': daily_fat,
        'meal_count': meal_count,
    }

    return render(request, 'core/view_diet_plan.html', context)

# Activate Diet Plan
@login_required
def activate_diet_plan(request, plan_id):
    diet_plan = get_object_or_404(DietPlan, id=plan_id, user=request.user)

    # Set all plans to inactive
    DietPlan.objects.filter(user=request.user).update(is_active=False)

    # Set this plan to active
    diet_plan.is_active = True
    diet_plan.save()

    messages.success(request, f'Diet plan "{diet_plan.name}" has been activated.')
    return redirect('view_diet_plan', plan_id=plan_id)

# Delete Diet Plan
@login_required
def delete_diet_plan(request, plan_id):
    diet_plan = get_object_or_404(DietPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        plan_name = diet_plan.name
        diet_plan.delete()
        messages.success(request, f'Diet plan "{plan_name}" has been deleted.')
        return redirect('dashboard')

    return render(request, 'core/delete_diet_plan.html', {'diet_plan': diet_plan})

# List Diet Plans
@login_required
def list_diet_plans(request):
    diet_plans = DietPlan.objects.filter(user=request.user).order_by('-is_active', '-created_at')

    return render(request, 'core/list_diet_plans.html', {'diet_plans': diet_plans})

# AI Coach View with OpenAI Integration
@login_required
def ai_coach(request):
    from .ai_helpers import get_chatbot_response

    user_message = request.GET.get('message', '')
    bot_response = ''

    if user_message:
        # Use OpenAI API for chatbot responses
        bot_response = get_chatbot_response(user_message)

    context = {
        'user_message': user_message,
        'bot_response': bot_response,
    }

    return render(request, 'core/ai_coach.html', context)

# Add Meals from AI-Generated Plan
@login_required
def add_meals_from_plan(request, plan_id):
    diet_plan = get_object_or_404(DietPlan, id=plan_id, user=request.user)

    if not diet_plan.description:
        messages.error(request, 'No AI-generated meal plan found.')
        return redirect('view_diet_plan', plan_id=plan_id)

    try:
        # Parse the AI-generated meal plan
        meal_plan_text = diet_plan.description

        # Clear existing meals from the plan
        DietPlanMeal.objects.filter(diet_plan=diet_plan).delete()

        # Parse the meal plan and add meals
        days = {}
        current_day = None
        current_meal_type = None
        meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

        # Track total nutrition for the plan
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        meal_count = 0

        # Simple parsing of the AI-generated meal plan
        lines = meal_plan_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                i += 1
                continue

            # Check for day headers
            if ('Day' in line and ':' in line) or ('##' in line and any(day in line for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])):
                # Map day names to numbers
                day_mapping = {
                    'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7
                }

                for day_name, day_num in day_mapping.items():
                    if day_name in line:
                        current_day = day_num
                        days[current_day] = []
                        break

            # Check for meal type headers
            elif 'Breakfast' in line:
                current_meal_type = 'B'
                meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

                # Look ahead for calorie information
                if i+1 < len(lines) and 'calories' in lines[i+1].lower():
                    try:
                        calorie_text = lines[i+1].lower()
                        if 'approx' in calorie_text and 'calories' in calorie_text:
                            calorie_str = calorie_text.split('approx')[1].split('calories')[0].strip(). \
                                          replace('(', '').replace(')', '').replace('.', '').strip()
                            meal_data['calories'] = int(calorie_str)
                    except (ValueError, IndexError):
                        pass

            elif 'Lunch' in line:
                current_meal_type = 'L'
                meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

                # Look ahead for calorie information
                if i+1 < len(lines) and 'calories' in lines[i+1].lower():
                    try:
                        calorie_text = lines[i+1].lower()
                        if 'approx' in calorie_text and 'calories' in calorie_text:
                            calorie_str = calorie_text.split('approx')[1].split('calories')[0].strip(). \
                                          replace('(', '').replace(')', '').replace('.', '').strip()
                            meal_data['calories'] = int(calorie_str)
                    except (ValueError, IndexError):
                        pass

            elif 'Dinner' in line:
                current_meal_type = 'D'
                meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

                # Look ahead for calorie information
                if i+1 < len(lines) and 'calories' in lines[i+1].lower():
                    try:
                        calorie_text = lines[i+1].lower()
                        if 'approx' in calorie_text and 'calories' in calorie_text:
                            calorie_str = calorie_text.split('approx')[1].split('calories')[0].strip(). \
                                          replace('(', '').replace(')', '').replace('.', '').strip()
                            meal_data['calories'] = int(calorie_str)
                    except (ValueError, IndexError):
                        pass

            elif 'Snack' in line or 'Snacks' in line:
                current_meal_type = 'S'
                meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

                # Look ahead for calorie information
                if i+1 < len(lines) and 'calories' in lines[i+1].lower():
                    try:
                        calorie_text = lines[i+1].lower()
                        if 'approx' in calorie_text and 'calories' in calorie_text:
                            calorie_str = calorie_text.split('approx')[1].split('calories')[0].strip(). \
                                          replace('(', '').replace(')', '').replace('.', '').strip()
                            meal_data['calories'] = int(calorie_str)
                    except (ValueError, IndexError):
                        pass

            # Extract meal details
            elif current_day is not None and current_meal_type is not None:
                # Extract dish name
                if ('**Dish' in line or '- **Dish' in line or line.startswith('- **') or 'Dish:' in line) and not meal_data['name']:
                    try:
                        if '**' in line:
                            parts = line.split('**')
                            if len(parts) >= 3:  # Format: - **Dish:** Name
                                meal_data['name'] = parts[2].strip().lstrip(':').strip()
                            elif len(parts) >= 2:  # Format: - **Name**
                                meal_data['name'] = parts[1].strip()
                        elif 'Dish:' in line:
                            meal_data['name'] = line.split('Dish:')[1].strip()
                    except (IndexError, ValueError):
                        pass

                # Extract ingredients
                elif ('**Ingredients' in line or 'Ingredients:' in line) and not meal_data['ingredients']:
                    try:
                        if '**' in line:
                            parts = line.split('**')
                            if len(parts) >= 3:  # Format: - **Ingredients:** List
                                meal_data['ingredients'] = parts[2].strip().lstrip(':').strip()
                        elif 'Ingredients:' in line:
                            meal_data['ingredients'] = line.split('Ingredients:')[1].strip()
                    except (IndexError, ValueError):
                        pass

                # Extract calories if not already set
                elif ('**Calories' in line or 'Calories:' in line) and meal_data['calories'] == 0:
                    try:
                        if '**' in line:
                            parts = line.split('**')
                            if len(parts) >= 3:  # Format: - **Calories:** 500
                                calorie_str = parts[2].strip().lstrip(':').strip()
                                meal_data['calories'] = int(calorie_str.split()[0])
                        elif 'Calories:' in line:
                            calorie_str = line.split('Calories:')[1].strip()
                            meal_data['calories'] = int(calorie_str.split()[0])
                    except (IndexError, ValueError):
                        pass

                # Extract macronutrients
                elif '**Macronutrients' in line or 'Macronutrients:' in line or 'Macros:' in line:
                    try:
                        macros_text = ''
                        if '**' in line:
                            parts = line.split('**')
                            if len(parts) >= 3:  # Format: - **Macronutrients:** Protein: 30g, Carbs: 40g, Fat: 15g
                                macros_text = parts[2].strip().lstrip(':').strip()
                        elif 'Macronutrients:' in line:
                            macros_text = line.split('Macronutrients:')[1].strip()
                        elif 'Macros:' in line:
                            macros_text = line.split('Macros:')[1].strip()

                        if macros_text:
                            # Extract protein
                            if 'protein' in macros_text.lower():
                                protein_part = macros_text.lower().split('protein')[1].split(',')[0].strip().lstrip(':').strip()
                                if 'g' in protein_part:
                                    meal_data['protein'] = float(protein_part.split('g')[0].strip())

                            # Extract carbs
                            if 'carbs' in macros_text.lower():
                                carbs_part = macros_text.lower().split('carbs')[1].split(',')[0].strip().lstrip(':').strip()
                                if 'g' in carbs_part:
                                    meal_data['carbs'] = float(carbs_part.split('g')[0].strip())

                            # Extract fat
                            if 'fat' in macros_text.lower():
                                fat_part = macros_text.lower().split('fat')[1].split(',')[0].strip().lstrip(':').strip()
                                if 'g' in fat_part:
                                    meal_data['fat'] = float(fat_part.split('g')[0].strip())
                    except (IndexError, ValueError):
                        pass

                # If we have a complete meal and we're at the end of a section or the file, add it to the plan
                next_line = lines[i+1].strip() if i+1 < len(lines) else ''
                is_section_end = not next_line or next_line.startswith('---') or next_line.startswith('#') or \
                                 'Breakfast' in next_line or 'Lunch' in next_line or 'Dinner' in next_line or \
                                 'Snack' in next_line or 'Day' in next_line

                if meal_data['name'] and meal_data['calories'] > 0 and current_day in days and \
                   (is_section_end or i == len(lines)-1):
                    # Try to find an existing meal with the same name for this user
                    try:
                        meal = Meal.objects.get(user=request.user, name=meal_data['name'])
                        # Update the meal with new data
                        if meal_data['ingredients']:
                            meal.description = meal_data['ingredients']
                            meal.calories = meal_data['calories']
                            meal.protein = meal_data['protein']
                            meal.carbs = meal_data['carbs']
                            meal.fat = meal_data['fat']
                            meal.meal_type = current_meal_type
                            meal.save()
                    except Meal.DoesNotExist:
                        # Create a new meal
                        meal = Meal.objects.create(
                            user=request.user,
                            name=meal_data['name'],
                            description=meal_data['ingredients'],
                            calories=meal_data['calories'],
                            protein=meal_data['protein'],
                            carbs=meal_data['carbs'],
                            fat=meal_data['fat'],
                            meal_type=current_meal_type,
                            is_public=False
                        )

                    # Add the meal to the diet plan
                    DietPlanMeal.objects.create(
                        diet_plan=diet_plan,
                        meal=meal,
                        day=current_day,
                        meal_type=current_meal_type
                    )

                    # Add to totals
                    total_calories += meal_data['calories']
                    total_protein += meal_data['protein']
                    total_carbs += meal_data['carbs']
                    total_fat += meal_data['fat']
                    meal_count += 1

                    # Reset meal data
                    meal_data = {'name': '', 'ingredients': '', 'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}

            i += 1

        # Update the diet plan with the calculated totals
        if meal_count > 0:
            # Calculate daily averages
            days_count = len(days)
            if days_count > 0:
                diet_plan.total_calories = total_calories // days_count
                diet_plan.total_protein = round(total_protein / days_count, 1)
                diet_plan.total_carbs = round(total_carbs / days_count, 1)
                diet_plan.total_fat = round(total_fat / days_count, 1)
                diet_plan.save()

        messages.success(request, f'Successfully added {meal_count} meals from the AI-generated plan to your diet plan.')
    except Exception as e:
        messages.error(request, f'Error adding meals from AI plan: {str(e)}')

    return redirect('view_diet_plan', plan_id=plan_id)

# AI Diet Plan Generation View
@login_required
def generate_ai_diet_plan(request):
    from .ai_helpers import generate_diet_plan

    user_profile = request.user.profile

    # If profile not completed, redirect to profile setup
    if not user_profile.profile_completed:
        messages.info(request, 'Please complete your profile first.')
        return redirect('profile_setup')

    try:
        diet_pref = DietPreference.objects.get(user=request.user)
    except DietPreference.DoesNotExist:
        diet_pref = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            messages.error(request, 'Please select start and end dates.')
            return redirect('generate_ai_diet_plan')

        # Create a new diet plan
        diet_plan = DietPlan(
            user=request.user,
            name=f"AI Diet Plan {start_date} to {end_date}",
            start_date=start_date,
            end_date=end_date,
            total_calories=user_profile.daily_calories,
            is_active=True
        )
        diet_plan.save()

        # Set all other plans to inactive
        DietPlan.objects.filter(user=request.user).exclude(id=diet_plan.id).update(is_active=False)

        try:
            # Generate AI diet plan
            ai_generated_plan = generate_diet_plan(user_profile, diet_pref)

            # Store the AI response in the diet plan description
            diet_plan.description = ai_generated_plan
            diet_plan.save()

            # Check if the response contains an error message
            if "API quota exceeded" in ai_generated_plan:
                messages.warning(request, 'OpenAI API quota exceeded. A fallback plan has been generated.')
            else:
                messages.success(request, 'AI Diet plan generated successfully!')

            return redirect('view_diet_plan', plan_id=diet_plan.id)
        except Exception as e:
            # If there's an error, delete the diet plan and redirect to the error page
            diet_plan.delete()
            error_message = str(e)

            # Check for specific API errors
            if "quota" in error_message.lower() or "insufficient_quota" in error_message:
                error_message = "OpenAI API quota exceeded. Please try again later or contact the administrator."
            elif "invalid_api_key" in error_message.lower():
                error_message = "Invalid OpenAI API key. Please contact the administrator."
            else:
                error_message = f"Error generating AI diet plan: {error_message}"

            return redirect(f'api-error/?error={error_message}')

    context = {
        'user_profile': user_profile,
        'diet_pref': diet_pref,
        'today': date.today().strftime('%Y-%m-%d'),
        'week_later': (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
    }

    return render(request, 'core/generate_ai_diet_plan.html', context)

# API Error View
@login_required
def api_error(request):
    error_message = request.GET.get('error', 'The OpenAI API service is currently unavailable.')
    return render(request, 'core/api_error.html', {'error_message': error_message})

# Mark Meal as Taken View
@login_required
def mark_meal_taken(request, meal_plan_id):
    # Get the meal plan item
    meal_plan = get_object_or_404(DietPlanMeal, id=meal_plan_id, diet_plan__user=request.user)

    # Create a meal log entry
    meal_log = MealLog(
        user=request.user,
        meal=meal_plan.meal,
        calories=meal_plan.meal.calories,
        protein=meal_plan.meal.protein,
        carbs=meal_plan.meal.carbs,
        fat=meal_plan.meal.fat,
        meal_type=meal_plan.meal_type,
        date=timezone.now().date(),
        time=timezone.now().time()
    )
    meal_log.save()

    messages.success(request, f'{meal_plan.meal.name} marked as taken!')
    return redirect('dashboard')
