from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/',views.home,name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('workout/', views.workout_view, name='workout'),
    path('meal-planner/', views.meal_planner, name='meal_planner'),
    path('meal-history/', views.meal_history, name='meal_history'),
    path('delete-meal/<int:pk>/', views.delete_meal, name='delete_meal'),
    path('water/', views.water, name='water'),
    path('bmi/', views.bmi, name='bmi'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
