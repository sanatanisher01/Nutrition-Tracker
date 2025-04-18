import os
import django
import sys

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutritrack.settings')
django.setup()

# Import Django models
from django.contrib.auth.models import User
from core.models import DietPlan, UserProfile, DietPreference
from datetime import date, timedelta

# AI-generated meal plan content
AI_MEAL_PLAN = """Here's a 7-day vegetarian meal plan tailored for an 18-year-old male aiming for weight loss, with a daily calorie target of approximately 2429 calories. Each day's meals are structured to meet the specified macronutrient distribution.

### **Day 1: Monday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Greek Yogurt Parfait
- **Ingredients:** 1 cup Greek yogurt, 1/2 cup mixed berries, 1/4 cup granola, 1 tbsp honey
- **Calories:** 607
- **Macronutrients:** Protein: 32g, Carbs: 82g, Fat: 14g

#### Lunch (Approx. 729 calories)
- **Dish:** Quinoa and Black Bean Salad
- **Ingredients:** 1 cup cooked quinoa, 1/2 cup black beans, 1/2 avocado, 1 cup cherry tomatoes, lime dressing
- **Calories:** 729
- **Macronutrients:** Protein: 24g, Carbs: 103g, Fat: 24g

#### Dinner (Approx. 729 calories)
- **Dish:** Vegetable Stir-fry with Tofu
- **Ingredients:** 200g firm tofu, 2 cups mixed vegetables (bell peppers, broccoli, carrots), 2 tbsp soy sauce, 1 tbsp olive oil
- **Calories:** 729
- **Macronutrients:** Protein: 38g, Carbs: 50g, Fat: 40g

#### Snacks (Approx. 364 calories)
- **Dish:** Hummus and Veggies
- **Ingredients:** 1/2 cup hummus, 1 cup carrot and cucumber sticks
- **Calories:** 364
- **Macronutrients:** Protein: 10g, Carbs: 45g, Fat: 18g

---

### **Day 2: Tuesday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Oatmeal with Almonds and Banana
- **Ingredients:** 1 cup cooked oats, 1 medium banana, 2 tbsp almond butter, 1 tbsp chia seeds
- **Calories:** 607
- **Macronutrients:** Protein: 20g, Carbs: 80g, Fat: 25g

#### Lunch (Approx. 729 calories)
- **Dish:** Mediterranean Chickpea Wrap
- **Ingredients:** 1 whole grain wrap, 3/4 cup chickpeas, 1/4 cup hummus, mixed greens, 1/4 cup feta cheese
- **Calories:** 729
- **Macronutrients:** Protein: 30g, Carbs: 90g, Fat: 28g

#### Dinner (Approx. 729 calories)
- **Dish:** Lentil and Vegetable Curry
- **Ingredients:** 1 cup cooked lentils, 1.5 cups mixed vegetables, 1/2 cup coconut milk, curry spices, 1/2 cup brown rice
- **Calories:** 729
- **Macronutrients:** Protein: 25g, Carbs: 110g, Fat: 20g

#### Snacks (Approx. 364 calories)
- **Dish:** Trail Mix
- **Ingredients:** 1/4 cup mixed nuts, 2 tbsp dried cranberries, 1 tbsp dark chocolate chips
- **Calories:** 364
- **Macronutrients:** Protein: 10g, Carbs: 30g, Fat: 25g

---

### **Day 3: Wednesday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Vegetarian Breakfast Burrito
- **Ingredients:** 1 whole grain tortilla, 1/2 cup scrambled tofu, 1/4 cup black beans, 1/4 avocado, salsa
- **Calories:** 607
- **Macronutrients:** Protein: 25g, Carbs: 70g, Fat: 25g

#### Lunch (Approx. 729 calories)
- **Dish:** Spinach and Feta Stuffed Baked Potato
- **Ingredients:** 1 large baked potato, 2 cups sautéed spinach, 1/3 cup feta cheese, 1 tbsp olive oil
- **Calories:** 729
- **Macronutrients:** Protein: 20g, Carbs: 100g, Fat: 30g

#### Dinner (Approx. 729 calories)
- **Dish:** Bean and Vegetable Enchiladas
- **Ingredients:** 2 corn tortillas, 1 cup mixed beans, 1 cup sautéed vegetables, 1/4 cup cheese, enchilada sauce
- **Calories:** 729
- **Macronutrients:** Protein: 30g, Carbs: 95g, Fat: 25g

#### Snacks (Approx. 364 calories)
- **Dish:** Greek Yogurt with Honey and Walnuts
- **Ingredients:** 3/4 cup Greek yogurt, 1 tbsp honey, 2 tbsp chopped walnuts
- **Calories:** 364
- **Macronutrients:** Protein: 20g, Carbs: 30g, Fat: 18g

---

### **Day 4: Thursday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Whole Grain Toast with Avocado and Eggs
- **Ingredients:** 2 slices whole grain bread, 1/2 avocado, 2 poached eggs, cherry tomatoes
- **Calories:** 607
- **Macronutrients:** Protein: 25g, Carbs: 60g, Fat: 30g

#### Lunch (Approx. 729 calories)
- **Dish:** Vegetarian Chili
- **Ingredients:** 1 cup mixed beans, 1 cup vegetables (onions, peppers, tomatoes), chili spices, 1/4 cup shredded cheese
- **Calories:** 729
- **Macronutrients:** Protein: 35g, Carbs: 90g, Fat: 25g

#### Dinner (Approx. 729 calories)
- **Dish:** Eggplant Parmesan with Quinoa
- **Ingredients:** 1 medium eggplant, 1/3 cup mozzarella cheese, marinara sauce, 3/4 cup cooked quinoa
- **Calories:** 729
- **Macronutrients:** Protein: 30g, Carbs: 80g, Fat: 30g

#### Snacks (Approx. 364 calories)
- **Dish:** Apple with Peanut Butter
- **Ingredients:** 1 large apple, 2 tbsp peanut butter
- **Calories:** 364
- **Macronutrients:** Protein: 8g, Carbs: 50g, Fat: 16g

---

### **Day 5: Friday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Smoothie Bowl
- **Ingredients:** 1 banana, 1 cup mixed berries, 1 scoop plant protein powder, 1 cup almond milk, 2 tbsp granola
- **Calories:** 607
- **Macronutrients:** Protein: 30g, Carbs: 85g, Fat: 15g

#### Lunch (Approx. 729 calories)
- **Dish:** Falafel Wrap
- **Ingredients:** 4 falafel balls, 1 whole grain wrap, 2 tbsp tahini sauce, lettuce, tomato, cucumber
- **Calories:** 729
- **Macronutrients:** Protein: 25g, Carbs: 90g, Fat: 30g

#### Dinner (Approx. 729 calories)
- **Dish:** Stuffed Bell Peppers
- **Ingredients:** 2 large bell peppers, 1 cup cooked brown rice, 1/2 cup black beans, 1/4 cup cheese, spices
- **Calories:** 729
- **Macronutrients:** Protein: 25g, Carbs: 100g, Fat: 25g

#### Snacks (Approx. 364 calories)
- **Dish:** Cottage Cheese with Fruit
- **Ingredients:** 1 cup low-fat cottage cheese, 1/2 cup pineapple chunks
- **Calories:** 364
- **Macronutrients:** Protein: 28g, Carbs: 30g, Fat: 10g

---

### **Day 6: Saturday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Vegetable Frittata
- **Ingredients:** 3 eggs, 1 cup mixed vegetables (spinach, tomatoes, onions), 1/4 cup feta cheese, 1 slice whole grain toast
- **Calories:** 607
- **Macronutrients:** Protein: 30g, Carbs: 50g, Fat: 35g

#### Lunch (Approx. 729 calories)
- **Dish:** Lentil Soup with Whole Grain Bread
- **Ingredients:** 1.5 cups lentil soup, 2 slices whole grain bread, 1 tbsp olive oil
- **Calories:** 729
- **Macronutrients:** Protein: 30g, Carbs: 100g, Fat: 20g

#### Dinner (Approx. 729 calories)
- **Dish:** Vegetable and Tofu Stir-Fry with Brown Rice
- **Ingredients:** 200g tofu, 2 cups mixed vegetables, 1 tbsp sesame oil, 1 cup cooked brown rice
- **Calories:** 729
- **Macronutrients:** Protein: 35g, Carbs: 90g, Fat: 25g

#### Snacks (Approx. 364 calories)
- **Dish:** Energy Balls
- **Ingredients:** 3 homemade energy balls (dates, nuts, cocoa powder, oats)
- **Calories:** 364
- **Macronutrients:** Protein: 10g, Carbs: 40g, Fat: 20g

---

### **Day 7: Sunday**

#### Breakfast (Approx. 607 calories)
- **Dish:** Whole Grain Pancakes with Fruit
- **Ingredients:** 3 whole grain pancakes, 1 cup mixed berries, 2 tbsp maple syrup, 1 tbsp almond butter
- **Calories:** 607
- **Macronutrients:** Protein: 20g, Carbs: 90g, Fat: 20g

#### Lunch (Approx. 729 calories)
- **Dish:** Caprese Sandwich
- **Ingredients:** 2 slices whole grain bread, 2 oz fresh mozzarella, tomato slices, basil, 1 tbsp olive oil, side salad
- **Calories:** 729
- **Macronutrients:** Protein: 25g, Carbs: 80g, Fat: 35g

#### Dinner (Approx. 729 calories)
- **Dish:** Vegetable Lasagna
- **Ingredients:** 1 serving vegetable lasagna (pasta, ricotta, vegetables, tomato sauce), side salad with vinaigrette
- **Calories:** 729
- **Macronutrients:** Protein: 30g, Carbs: 85g, Fat: 30g

#### Snacks (Approx. 364 calories)
- **Dish:** Roasted Chickpeas
- **Ingredients:** 3/4 cup roasted chickpeas with spices, 1 small piece of dark chocolate
- **Calories:** 364
- **Macronutrients:** Protein: 15g, Carbs: 45g, Fat: 15g"""

def add_ai_meal_plan():
    try:
        # Get the first user (or create one if none exists)
        user = User.objects.first()
        if not user:
            print("No users found in the database. Please create a user first.")
            return
        
        # Get user profile
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            print(f"No profile found for user {user.username}")
            return
        
        # Create a new diet plan
        start_date = date.today()
        end_date = start_date + timedelta(days=7)
        
        diet_plan = DietPlan(
            user=user,
            name=f"AI Diet Plan {start_date} to {end_date}",
            start_date=start_date,
            end_date=end_date,
            total_calories=user_profile.daily_calories or 2429,
            is_active=True,
            description=AI_MEAL_PLAN
        )
        diet_plan.save()
        
        # Set all other plans to inactive
        DietPlan.objects.filter(user=user).exclude(id=diet_plan.id).update(is_active=False)
        
        print(f"AI meal plan created successfully with ID: {diet_plan.id}")
        print(f"View it at: http://127.0.0.1:8080/diet-plan/{diet_plan.id}/")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    add_ai_meal_plan()
