# Generated by Django 5.2 on 2025-04-18 04:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('calories_per_100g', models.PositiveIntegerField(default=0)),
                ('protein_per_100g', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('carbs_per_100g', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fat_per_100g', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('is_vegetarian', models.BooleanField(default=True)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_gluten_free', models.BooleanField(default=True)),
                ('is_dairy_free', models.BooleanField(default=True)),
                ('is_nut_free', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_calories', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DietPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diet_type', models.CharField(choices=[('R', 'Regular (No Restrictions)'), ('V', 'Vegetarian'), ('VG', 'Vegan'), ('E', 'Eggetarian'), ('P', 'Pescatarian'), ('K', 'Keto'), ('PL', 'Paleo')], default='R', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('allergies', models.ManyToManyField(blank=True, to='core.allergen')),
                ('preferred_cuisines', models.ManyToManyField(blank=True, to='core.cuisine')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diet_preference', to=settings.AUTH_USER_MODEL)),
                ('disliked_ingredients', models.ManyToManyField(blank=True, related_name='disliked_by', to='core.ingredient')),
                ('favorite_ingredients', models.ManyToManyField(blank=True, related_name='favorite_of', to='core.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('meal_type', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack')], max_length=1)),
                ('calories', models.PositiveIntegerField()),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('preparation_time', models.PositiveIntegerField(help_text='Time in minutes')),
                ('cooking_time', models.PositiveIntegerField(help_text='Time in minutes')),
                ('instructions', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='meal_images/')),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_gluten_free', models.BooleanField(default=False)),
                ('is_dairy_free', models.BooleanField(default=False)),
                ('is_nut_free', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cuisines', models.ManyToManyField(blank=True, to='core.cuisine')),
            ],
        ),
        migrations.CreateModel(
            name='MealIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6)),
                ('unit', models.CharField(max_length=50)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ingredient')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.meal')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.ManyToManyField(through='core.MealIngredient', to='core.ingredient'),
        ),
        migrations.CreateModel(
            name='MealLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_meal_name', models.CharField(blank=True, max_length=200)),
                ('calories', models.PositiveIntegerField()),
                ('protein', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('carbs', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('meal_type', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack')], max_length=1)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('notes', models.TextField(blank=True)),
                ('meal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-time'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('height', models.PositiveIntegerField(blank=True, help_text='Height in centimeters', null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Weight in kilograms', max_digits=5, null=True)),
                ('activity_level', models.CharField(blank=True, choices=[('S', 'Sedentary (little or no exercise)'), ('L', 'Lightly active (light exercise/sports 1-3 days/week)'), ('M', 'Moderately active (moderate exercise/sports 3-5 days/week)'), ('V', 'Very active (hard exercise/sports 6-7 days a week)'), ('E', 'Extra active (very hard exercise & physical job or 2x training)')], max_length=1, null=True)),
                ('goal', models.CharField(blank=True, choices=[('L', 'Weight Loss'), ('M', 'Maintenance'), ('G', 'Muscle Gain')], max_length=1, null=True)),
                ('daily_calories', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DietPlanMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('meal_type', models.CharField(choices=[('B', 'Breakfast'), ('L', 'Lunch'), ('D', 'Dinner'), ('S', 'Snack')], max_length=1)),
                ('diet_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='core.dietplan')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.meal')),
            ],
            options={
                'unique_together': {('diet_plan', 'day', 'meal_type')},
            },
        ),
        migrations.CreateModel(
            name='WeightLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, help_text='Weight in kilograms', max_digits=5)),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
