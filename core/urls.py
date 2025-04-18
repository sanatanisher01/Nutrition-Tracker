from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calorie-calculator/', views.calorie_calculator, name='calorie_calculator'),
    path('meal-library/', views.meal_library, name='meal_library'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        authentication_form=UserLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # User profile and preferences
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('diet-preferences/', views.diet_preferences, name='diet_preferences'),
    path('profile/', views.profile, name='profile'),

    # Dashboard and tracking
    path('dashboard/', views.dashboard, name='dashboard'),
    path('weight-log/', views.weight_log, name='weight_log'),
    path('meal-log/', views.meal_log, name='meal_log'),

    # Diet plans
    path('generate-diet-plan/', views.generate_diet_plan, name='generate_diet_plan'),
    path('generate-ai-diet-plan/', views.generate_ai_diet_plan, name='generate_ai_diet_plan'),
    path('diet-plan/<int:plan_id>/', views.view_diet_plan, name='view_diet_plan'),
    path('diet-plan/<int:plan_id>/activate/', views.activate_diet_plan, name='activate_diet_plan'),
    path('diet-plan/<int:plan_id>/delete/', views.delete_diet_plan, name='delete_diet_plan'),
    path('diet-plan/<int:plan_id>/add-meals/', views.add_meals_from_plan, name='add_meals_from_plan'),
    path('diet-plans/', views.list_diet_plans, name='list_diet_plans'),

    # AI Coach
    path('ai-coach/', views.ai_coach, name='ai_coach'),

    # Mark meal as taken
    path('diet-plan-meal/<int:meal_plan_id>/mark-taken/', views.mark_meal_taken, name='mark_meal_taken'),
]
