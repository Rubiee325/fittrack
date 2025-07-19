# core/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Workout)
admin.site.register(WorkoutLog)
admin.site.register(WaterGoal)
admin.site.register(WaterIntake)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'calories', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('name', 'user__username', 'category')


# Register your models here.
