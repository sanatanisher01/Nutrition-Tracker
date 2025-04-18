import os
import django
import sys

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

# Import Django models
from core.models import DietPlan

def update_diet_plans():
    # Get all diet plans
    diet_plans = DietPlan.objects.all()
    
    for plan in diet_plans:
        # Calculate default macronutrient values based on calories
        # Using standard macronutrient distribution: 30% protein, 40% carbs, 30% fat
        total_calories = plan.total_calories
        
        # Calculate grams of each macronutrient
        # Protein: 4 calories per gram, Carbs: 4 calories per gram, Fat: 9 calories per gram
        protein_calories = total_calories * 0.30
        carbs_calories = total_calories * 0.40
        fat_calories = total_calories * 0.30
        
        protein_grams = round(protein_calories / 4, 1)
        carbs_grams = round(carbs_calories / 4, 1)
        fat_grams = round(fat_calories / 9, 1)
        
        # Update the diet plan
        plan.total_protein = protein_grams
        plan.total_carbs = carbs_grams
        plan.total_fat = fat_grams
        plan.save()
        
        print(f"Updated Plan ID: {plan.id}, Name: {plan.name}")
        print(f"  Calories: {plan.total_calories}")
        print(f"  Protein: {plan.total_protein}g")
        print(f"  Carbs: {plan.total_carbs}g")
        print(f"  Fat: {plan.total_fat}g")
        print()

if __name__ == "__main__":
    update_diet_plans()
    print("All diet plans have been updated with default nutritional values.")
