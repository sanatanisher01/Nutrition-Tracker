import os
import django
import sys

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

# Import Django models
from django.contrib.auth.models import User
from core.models import DietPlan, Meal, DietPlanMeal

def add_sample_meals():
    # Get the first user (or create one if none exists)
    user = User.objects.first()
    if not user:
        print("No users found in the database. Please create a user first.")
        return
    
    # Get the diet plan (use the first active plan)
    try:
        diet_plan = DietPlan.objects.filter(user=user, is_active=True).first()
        if not diet_plan:
            diet_plan = DietPlan.objects.filter(user=user).first()
        
        if not diet_plan:
            print("No diet plans found for this user.")
            return
    except Exception as e:
        print(f"Error finding diet plan: {str(e)}")
        return
    
    print(f"Adding sample meals to diet plan: {diet_plan.name} (ID: {diet_plan.id})")
    
    # Clear existing meals from the plan
    DietPlanMeal.objects.filter(diet_plan=diet_plan).delete()
    
    # Sample meals for each day of the week
    sample_meals = [
        # Day 1 (Monday)
        {
            'day': 1,
            'meals': [
                {'name': 'Greek Yogurt Parfait', 'type': 'B', 'calories': 607, 'protein': 32, 'carbs': 82, 'fat': 14, 
                 'description': '1 cup Greek yogurt, 1/2 cup mixed berries, 1/4 cup granola, 1 tbsp honey'},
                {'name': 'Quinoa and Black Bean Salad', 'type': 'L', 'calories': 729, 'protein': 24, 'carbs': 103, 'fat': 24,
                 'description': '1 cup cooked quinoa, 1/2 cup black beans, 1/2 avocado, 1 cup cherry tomatoes, lime dressing'},
                {'name': 'Vegetable Stir-fry with Tofu', 'type': 'D', 'calories': 729, 'protein': 38, 'carbs': 50, 'fat': 40,
                 'description': '200g firm tofu, 2 cups mixed vegetables (bell peppers, broccoli, carrots), 2 tbsp soy sauce, 1 tbsp olive oil'},
                {'name': 'Hummus and Veggies', 'type': 'S', 'calories': 364, 'protein': 10, 'carbs': 45, 'fat': 18,
                 'description': '1/2 cup hummus, 1 cup carrot and cucumber sticks'}
            ]
        },
        # Day 2 (Tuesday)
        {
            'day': 2,
            'meals': [
                {'name': 'Oatmeal with Almonds and Banana', 'type': 'B', 'calories': 607, 'protein': 20, 'carbs': 80, 'fat': 25,
                 'description': '1 cup cooked oats, 1 medium banana, 2 tbsp almond butter, 1 tbsp chia seeds'},
                {'name': 'Mediterranean Chickpea Wrap', 'type': 'L', 'calories': 729, 'protein': 30, 'carbs': 90, 'fat': 28,
                 'description': '1 whole grain wrap, 3/4 cup chickpeas, 1/4 cup hummus, mixed greens, 1/4 cup feta cheese'},
                {'name': 'Lentil and Vegetable Curry', 'type': 'D', 'calories': 729, 'protein': 25, 'carbs': 110, 'fat': 20,
                 'description': '1 cup cooked lentils, 1.5 cups mixed vegetables, 1/2 cup coconut milk, curry spices, 1/2 cup brown rice'},
                {'name': 'Trail Mix', 'type': 'S', 'calories': 364, 'protein': 10, 'carbs': 30, 'fat': 25,
                 'description': '1/4 cup mixed nuts, 2 tbsp dried cranberries, 1 tbsp dark chocolate chips'}
            ]
        },
        # Day 3 (Wednesday)
        {
            'day': 3,
            'meals': [
                {'name': 'Vegetarian Breakfast Burrito', 'type': 'B', 'calories': 607, 'protein': 25, 'carbs': 70, 'fat': 25,
                 'description': '1 whole grain tortilla, 1/2 cup scrambled tofu, 1/4 cup black beans, 1/4 avocado, salsa'},
                {'name': 'Spinach and Feta Stuffed Baked Potato', 'type': 'L', 'calories': 729, 'protein': 20, 'carbs': 100, 'fat': 30,
                 'description': '1 large baked potato, 2 cups sautéed spinach, 1/3 cup feta cheese, 1 tbsp olive oil'},
                {'name': 'Bean and Vegetable Enchiladas', 'type': 'D', 'calories': 729, 'protein': 30, 'carbs': 95, 'fat': 25,
                 'description': '2 corn tortillas, 1 cup mixed beans, 1 cup sautéed vegetables, 1/4 cup cheese, enchilada sauce'},
                {'name': 'Greek Yogurt with Honey and Walnuts', 'type': 'S', 'calories': 364, 'protein': 20, 'carbs': 30, 'fat': 18,
                 'description': '3/4 cup Greek yogurt, 1 tbsp honey, 2 tbsp chopped walnuts'}
            ]
        },
        # Day 4 (Thursday)
        {
            'day': 4,
            'meals': [
                {'name': 'Whole Grain Toast with Avocado and Eggs', 'type': 'B', 'calories': 607, 'protein': 25, 'carbs': 60, 'fat': 30,
                 'description': '2 slices whole grain bread, 1/2 avocado, 2 poached eggs, cherry tomatoes'},
                {'name': 'Vegetarian Chili', 'type': 'L', 'calories': 729, 'protein': 35, 'carbs': 90, 'fat': 25,
                 'description': '1 cup mixed beans, 1 cup vegetables (onions, peppers, tomatoes), chili spices, 1/4 cup shredded cheese'},
                {'name': 'Eggplant Parmesan with Quinoa', 'type': 'D', 'calories': 729, 'protein': 30, 'carbs': 80, 'fat': 30,
                 'description': '1 medium eggplant, 1/3 cup mozzarella cheese, marinara sauce, 3/4 cup cooked quinoa'},
                {'name': 'Apple with Peanut Butter', 'type': 'S', 'calories': 364, 'protein': 8, 'carbs': 50, 'fat': 16,
                 'description': '1 large apple, 2 tbsp peanut butter'}
            ]
        },
        # Day 5 (Friday)
        {
            'day': 5,
            'meals': [
                {'name': 'Smoothie Bowl', 'type': 'B', 'calories': 607, 'protein': 30, 'carbs': 85, 'fat': 15,
                 'description': '1 banana, 1 cup mixed berries, 1 scoop plant protein powder, 1 cup almond milk, 2 tbsp granola'},
                {'name': 'Falafel Wrap', 'type': 'L', 'calories': 729, 'protein': 25, 'carbs': 90, 'fat': 30,
                 'description': '4 falafel balls, 1 whole grain wrap, 2 tbsp tahini sauce, lettuce, tomato, cucumber'},
                {'name': 'Stuffed Bell Peppers', 'type': 'D', 'calories': 729, 'protein': 25, 'carbs': 100, 'fat': 25,
                 'description': '2 large bell peppers, 1 cup cooked brown rice, 1/2 cup black beans, 1/4 cup cheese, spices'},
                {'name': 'Cottage Cheese with Fruit', 'type': 'S', 'calories': 364, 'protein': 28, 'carbs': 30, 'fat': 10,
                 'description': '1 cup low-fat cottage cheese, 1/2 cup pineapple chunks'}
            ]
        },
        # Day 6 (Saturday)
        {
            'day': 6,
            'meals': [
                {'name': 'Vegetable Frittata', 'type': 'B', 'calories': 607, 'protein': 30, 'carbs': 50, 'fat': 35,
                 'description': '3 eggs, 1 cup mixed vegetables (spinach, tomatoes, onions), 1/4 cup feta cheese, 1 slice whole grain toast'},
                {'name': 'Lentil Soup with Whole Grain Bread', 'type': 'L', 'calories': 729, 'protein': 30, 'carbs': 100, 'fat': 20,
                 'description': '1.5 cups lentil soup, 2 slices whole grain bread, 1 tbsp olive oil'},
                {'name': 'Vegetable and Tofu Stir-Fry with Brown Rice', 'type': 'D', 'calories': 729, 'protein': 35, 'carbs': 90, 'fat': 25,
                 'description': '200g tofu, 2 cups mixed vegetables, 1 tbsp sesame oil, 1 cup cooked brown rice'},
                {'name': 'Energy Balls', 'type': 'S', 'calories': 364, 'protein': 10, 'carbs': 40, 'fat': 20,
                 'description': '3 homemade energy balls (dates, nuts, cocoa powder, oats)'}
            ]
        },
        # Day 7 (Sunday)
        {
            'day': 7,
            'meals': [
                {'name': 'Whole Grain Pancakes with Fruit', 'type': 'B', 'calories': 607, 'protein': 20, 'carbs': 90, 'fat': 20,
                 'description': '3 whole grain pancakes, 1 cup mixed berries, 2 tbsp maple syrup, 1 tbsp almond butter'},
                {'name': 'Caprese Sandwich', 'type': 'L', 'calories': 729, 'protein': 25, 'carbs': 80, 'fat': 35,
                 'description': '2 slices whole grain bread, 2 oz fresh mozzarella, tomato slices, basil, 1 tbsp olive oil, side salad'},
                {'name': 'Vegetable Lasagna', 'type': 'D', 'calories': 729, 'protein': 30, 'carbs': 85, 'fat': 30,
                 'description': '1 serving vegetable lasagna (pasta, ricotta, vegetables, tomato sauce), side salad with vinaigrette'},
                {'name': 'Roasted Chickpeas', 'type': 'S', 'calories': 364, 'protein': 15, 'carbs': 45, 'fat': 15,
                 'description': '3/4 cup roasted chickpeas with spices, 1 small piece of dark chocolate'}
            ]
        }
    ]
    
    # Add meals to the diet plan
    total_meals_added = 0
    
    for day_data in sample_meals:
        day = day_data['day']
        for meal_data in day_data['meals']:
            # Create or get the meal
            meal, created = Meal.objects.get_or_create(
                user=user,
                name=meal_data['name'],
                defaults={
                    'description': meal_data['description'],
                    'meal_type': meal_data['type'],
                    'calories': meal_data['calories'],
                    'protein': meal_data['protein'],
                    'carbs': meal_data['carbs'],
                    'fat': meal_data['fat'],
                    'is_vegetarian': True,
                    'is_public': False,
                    'preparation_time': 15,
                    'cooking_time': 20
                }
            )
            
            # If the meal already exists but we have new data, update it
            if not created:
                meal.description = meal_data['description']
                meal.meal_type = meal_data['type']
                meal.calories = meal_data['calories']
                meal.protein = meal_data['protein']
                meal.carbs = meal_data['carbs']
                meal.fat = meal_data['fat']
                meal.save()
            
            # Add the meal to the diet plan
            DietPlanMeal.objects.create(
                diet_plan=diet_plan,
                meal=meal,
                day=day,
                meal_type=meal_data['type']
            )
            
            total_meals_added += 1
    
    # Calculate and update the diet plan's nutritional information
    # Calculate average daily values
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for day_data in sample_meals:
        day_calories = sum(meal['calories'] for meal in day_data['meals'])
        day_protein = sum(meal['protein'] for meal in day_data['meals'])
        day_carbs = sum(meal['carbs'] for meal in day_data['meals'])
        day_fat = sum(meal['fat'] for meal in day_data['meals'])
        
        total_calories += day_calories
        total_protein += day_protein
        total_carbs += day_carbs
        total_fat += day_fat
    
    # Calculate daily averages
    days_count = len(sample_meals)
    diet_plan.total_calories = total_calories // days_count
    diet_plan.total_protein = round(total_protein / days_count, 1)
    diet_plan.total_carbs = round(total_carbs / days_count, 1)
    diet_plan.total_fat = round(total_fat / days_count, 1)
    diet_plan.save()
    
    print(f"Successfully added {total_meals_added} meals to the diet plan.")
    print(f"Updated diet plan nutritional information:")
    print(f"  Daily Calories: {diet_plan.total_calories}")
    print(f"  Daily Protein: {diet_plan.total_protein}g")
    print(f"  Daily Carbs: {diet_plan.total_carbs}g")
    print(f"  Daily Fat: {diet_plan.total_fat}g")
    print(f"View the diet plan at: http://127.0.0.1:8080/diet-plan/{diet_plan.id}/")

if __name__ == "__main__":
    add_sample_meals()
