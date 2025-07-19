from django import forms
from .models import *

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'
        exclude = ['user']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'input-field'}),
            'height': forms.NumberInput(attrs={'class': 'input-field'}),
            'weight': forms.NumberInput(attrs={'class': 'input-field'}),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'name', 'category', 'calories', 'carbs', 'protein', 'fats', 'image']
        exclude = ['user', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WaterGoalForm(forms.ModelForm):
    class Meta:
        model = WaterGoal
        fields = ['daily_goal']
        widgets = {
            'daily_goal': forms.NumberInput(attrs={
                'placeholder': 'Enter daily goal in ml',
                'class': 'form-control'
            }),
        }

class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterIntake
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter water intake in ml',
                'class': 'form-control'
            }),
        }

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['workout', 'progress']
        widgets = {
            'progress': forms.Textarea(attrs={'placeholder': 'Enter your progress details...', 'rows': 3}),
        }

class BMICalculatorForm(forms.Form):
    height = forms.FloatField(label="Height (cm)", min_value=1)
    weight = forms.FloatField(label="Weight (kg)", min_value=1)

