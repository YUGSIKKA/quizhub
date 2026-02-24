from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:quiz_id>/', views.result_view, name='result'),
    path('leaderboard/<int:quiz_id>/', views.leaderboard, name='leaderboard'),
]