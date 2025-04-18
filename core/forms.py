from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, DietPreference, WeightLog, MealLog, Meal

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# User Login Form
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

# User Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'gender', 'height', 'weight', 'activity_level', 'goal')
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'min': 50, 'max': 300, 'placeholder': 'cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 500, 'step': '0.1', 'placeholder': 'kg'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
        }

# Diet Preference Form
class DietPreferenceForm(forms.ModelForm):
    class Meta:
        model = DietPreference
        fields = ('diet_type', 'allergies', 'preferred_cuisines', 'disliked_ingredients', 'favorite_ingredients')
        widgets = {
            'diet_type': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'preferred_cuisines': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'disliked_ingredients': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'favorite_ingredients': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

# Weight Log Form
class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ('weight', 'date', 'notes')
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 500, 'step': '0.1', 'placeholder': 'kg'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Meal Log Form
class MealLogForm(forms.ModelForm):
    meal = forms.ModelChoiceField(
        queryset=Meal.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = MealLog
        fields = ('meal', 'custom_meal_name', 'calories', 'protein', 'carbs', 'fat', 'meal_type', 'date', 'time', 'notes')
        widgets = {
            'custom_meal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter meal name if not selecting from list'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.1'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.1'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        meal = cleaned_data.get('meal')
        custom_meal_name = cleaned_data.get('custom_meal_name')
        
        if not meal and not custom_meal_name:
            raise forms.ValidationError("Either select a meal or enter a custom meal name.")
        
        return cleaned_data

# BMR Calculator Form
class BMRCalculatorForm(forms.Form):
    GENDER_CHOICES = UserProfile.GENDER_CHOICES
    ACTIVITY_LEVEL_CHOICES = UserProfile.ACTIVITY_LEVEL_CHOICES
    GOAL_CHOICES = UserProfile.GOAL_CHOICES
    
    age = forms.IntegerField(
        min_value=1, 
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    height = forms.IntegerField(
        min_value=50,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height (cm)'})
    )
    weight = forms.DecimalField(
        min_value=20,
        max_value=500,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)', 'step': '0.1'})
    )
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        weight = float(self.cleaned_data['weight'])
        height = float(self.cleaned_data['height'])
        age = int(self.cleaned_data['age'])
        gender = self.cleaned_data['gender']
        
        if gender == 'M':
            return (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:  # Female or Other
            return (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        activity_level = self.cleaned_data['activity_level']
        
        activity_multipliers = {
            'S': 1.2,    # Sedentary
            'L': 1.375,  # Lightly active
            'M': 1.55,   # Moderately active
            'V': 1.725,  # Very active
            'E': 1.9     # Extra active
        }
        
        return int(bmr * activity_multipliers.get(activity_level, 1.2))
    
    def calculate_daily_calories(self):
        """Calculate daily calorie target based on TDEE and goal"""
        tdee = self.calculate_tdee()
        goal = self.cleaned_data['goal']
        
        goal_adjustments = {
            'L': -500,    # Weight Loss: deficit of 500 calories
            'M': 0,       # Maintenance: no adjustment
            'G': 500      # Muscle Gain: surplus of 500 calories
        }
        
        return tdee + goal_adjustments.get(goal, 0)

# Meal Search Form
class MealSearchForm(forms.Form):
    MEAL_TYPE_CHOICES = [('', 'All Types')] + list(Meal.MEAL_TYPE_CHOICES)
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search meals...'})
    )
    meal_type = forms.ChoiceField(
        choices=MEAL_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_calories = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min calories'})
    )
    max_calories = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max calories'})
    )
    is_vegetarian = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_vegan = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_gluten_free = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    cuisine = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super(MealSearchForm, self).__init__(*args, **kwargs)
        from .models import Cuisine
        self.fields['cuisine'].queryset = Cuisine.objects.all()

# Contact Form
class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'})
    )
