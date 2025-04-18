from django.contrib import admin
from .models import (
    UserProfile, DietPreference, Allergen, Cuisine, Ingredient,
    Meal, MealIngredient, DietPlan, DietPlanMeal, WeightLog, MealLog
)

# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'height', 'weight', 'activity_level', 'goal', 'daily_calories', 'profile_completed')
    list_filter = ('gender', 'activity_level', 'goal', 'profile_completed')
    search_fields = ('user__username', 'user__email')

# DietPreference Admin
class DietPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'diet_type')
    list_filter = ('diet_type',)
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('allergies', 'preferred_cuisines', 'disliked_ingredients', 'favorite_ingredients')

# Allergen Admin
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Cuisine Admin
class CuisineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Ingredient Admin
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories_per_100g', 'protein_per_100g', 'carbs_per_100g', 'fat_per_100g',
                   'is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_dairy_free', 'is_nut_free')
    list_filter = ('is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_dairy_free', 'is_nut_free')
    search_fields = ('name',)

# MealIngredient Inline for Meal Admin
class MealIngredientInline(admin.TabularInline):
    model = MealIngredient
    extra = 1

# Meal Admin
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_type', 'calories', 'protein', 'carbs', 'fat',
                   'is_vegetarian', 'is_vegan', 'is_gluten_free')
    list_filter = ('meal_type', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'cuisines')
    search_fields = ('name', 'description')
    inlines = [MealIngredientInline]
    filter_horizontal = ('cuisines',)

# DietPlanMeal Inline for DietPlan Admin
class DietPlanMealInline(admin.TabularInline):
    model = DietPlanMeal
    extra = 1

# DietPlan Admin
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'total_calories', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'user__username')
    inlines = [DietPlanMealInline]

# WeightLog Admin
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date')
    list_filter = ('date',)
    search_fields = ('user__username',)
    date_hierarchy = 'date'

# MealLog Admin
class MealLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_meal_name', 'meal_type', 'calories', 'date', 'time')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'custom_meal_name', 'meal__name')
    date_hierarchy = 'date'

    def get_meal_name(self, obj):
        return obj.meal.name if obj.meal else obj.custom_meal_name
    get_meal_name.short_description = 'Meal'

# Register models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DietPreference, DietPreferenceAdmin)
admin.site.register(Allergen, AllergenAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(DietPlan, DietPlanAdmin)
admin.site.register(WeightLog, WeightLogAdmin)
admin.site.register(MealLog, MealLogAdmin)
