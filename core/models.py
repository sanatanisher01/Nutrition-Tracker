from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    ACTIVITY_LEVEL_CHOICES = (
        ('S', 'Sedentary (little or no exercise)'),
        ('L', 'Lightly active (light exercise/sports 1-3 days/week)'),
        ('M', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        ('V', 'Very active (hard exercise/sports 6-7 days a week)'),
        ('E', 'Extra active (very hard exercise & physical job or 2x training)'),
    )

    GOAL_CHOICES = (
        ('L', 'Weight Loss'),
        ('M', 'Maintenance'),
        ('G', 'Muscle Gain'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.PositiveIntegerField(help_text="Height in centimeters", null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kilograms", null=True, blank=True)
    activity_level = models.CharField(max_length=1, choices=ACTIVITY_LEVEL_CHOICES, null=True, blank=True)
    goal = models.CharField(max_length=1, choices=GOAL_CHOICES, null=True, blank=True)
    daily_calories = models.PositiveIntegerField(null=True, blank=True)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if not all([self.age, self.gender, self.height, self.weight]):
            return None

        weight = float(self.weight)
        height = float(self.height)
        age = int(self.age)

        if self.gender == 'M':
            return (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:  # Female or Other
            return (10 * weight) + (6.25 * height) - (5 * age) - 161

    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        if not bmr:
            return None

        activity_multipliers = {
            'S': 1.2,    # Sedentary
            'L': 1.375,  # Lightly active
            'M': 1.55,   # Moderately active
            'V': 1.725,  # Very active
            'E': 1.9     # Extra active
        }

        return int(bmr * activity_multipliers.get(self.activity_level, 1.2))

    def calculate_daily_calories(self):
        """Calculate daily calorie target based on TDEE and goal"""
        tdee = self.calculate_tdee()
        if not tdee:
            return None

        goal_adjustments = {
            'L': -500,    # Weight Loss: deficit of 500 calories
            'M': 0,       # Maintenance: no adjustment
            'G': 500      # Muscle Gain: surplus of 500 calories
        }

        return tdee + goal_adjustments.get(self.goal, 0)

    def update_daily_calories(self):
        """Update the daily_calories field based on current stats"""
        calories = self.calculate_daily_calories()
        if calories:
            self.daily_calories = calories
            self.save(update_fields=['daily_calories'])

# Create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Diet Preferences Model
class DietPreference(models.Model):
    DIET_TYPE_CHOICES = (
        ('R', 'Regular (No Restrictions)'),
        ('V', 'Vegetarian'),
        ('VG', 'Vegan'),
        ('E', 'Eggetarian'),
        ('P', 'Pescatarian'),
        ('K', 'Keto'),
        ('PL', 'Paleo'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='diet_preference')
    diet_type = models.CharField(max_length=2, choices=DIET_TYPE_CHOICES, default='R')
    allergies = models.ManyToManyField('Allergen', blank=True)
    preferred_cuisines = models.ManyToManyField('Cuisine', blank=True)
    disliked_ingredients = models.ManyToManyField('Ingredient', blank=True, related_name='disliked_by')
    favorite_ingredients = models.ManyToManyField('Ingredient', blank=True, related_name='favorite_of')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Diet Preferences"

# Allergen Model
class Allergen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Cuisine Model
class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories_per_100g = models.PositiveIntegerField(default=0)
    protein_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbs_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat_per_100g = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_vegetarian = models.BooleanField(default=True)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=True)
    is_dairy_free = models.BooleanField(default=True)
    is_nut_free = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Meal Model
class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('S', 'Snack'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meals', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE_CHOICES, null=True, blank=True)
    calories = models.PositiveIntegerField(default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ingredients = models.ManyToManyField('Ingredient', through='MealIngredient', blank=True)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes", default=0)
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes", default=0)
    instructions = models.TextField(blank=True)
    image = models.ImageField(upload_to='meal_images/', null=True, blank=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_dairy_free = models.BooleanField(default=False)
    is_nut_free = models.BooleanField(default=False)
    cuisines = models.ManyToManyField('Cuisine', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# MealIngredient (Junction table between Meal and Ingredient)
class MealIngredient(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} for {self.meal.name}"

# DietPlan Model
class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_plans')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_calories = models.PositiveIntegerField()
    total_protein = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total_carbs = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    total_fat = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"

# DietPlanMeal (Junction table between DietPlan and Meal)
class DietPlanMeal(models.Model):
    DAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    diet_plan = models.ForeignKey('DietPlan', on_delete=models.CASCADE, related_name='meals')
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=1, choices=Meal.MEAL_TYPE_CHOICES)

    class Meta:
        unique_together = ('diet_plan', 'day', 'meal_type')

    def __str__(self):
        return f"{self.get_day_display()} {self.get_meal_type_display()} - {self.meal.name}"

# WeightLog Model
class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kilograms")
    date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s weight on {self.date}: {self.weight} kg"

# MealLog Model
class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_logs')
    meal = models.ForeignKey('Meal', on_delete=models.SET_NULL, null=True, blank=True)
    custom_meal_name = models.CharField(max_length=200, blank=True)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    meal_type = models.CharField(max_length=1, choices=Meal.MEAL_TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        meal_name = self.meal.name if self.meal else self.custom_meal_name
        return f"{self.user.username}'s {self.get_meal_type_display()} on {self.date}: {meal_name}"
