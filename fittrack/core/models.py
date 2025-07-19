from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    progress = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} - {self.date}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)


    def __str__(self):
        return self.user.username
    

class MealCategory(models.TextChoices):
    FRUITS = "Fruits"
    GRAINS = "Grains"
    PROTEIN = "Protein"
    VEGETABLES = "Vegetables"
    DAIRY = "Dairy"
    SNACK = "Snack"
    BEVERAGE = "Beverage"
    OTHER = "Other"

class Meal(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Grains', 'Grains'),
        ('Protein', 'Protein'),
        ('Vegetables', 'Vegetables'),
        ('Dairy', 'Dairy'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    calories = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

class WaterGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_goal = models.PositiveIntegerField(default=2000)  # in milliliters

    def __str__(self):
        return f"{self.user.username}'s Goal: {self.daily_goal} ml"

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # in milliliters
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ml on {self.date}"

