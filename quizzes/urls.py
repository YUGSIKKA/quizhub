from django.urls import path
from . import views

urlpatterns = [
    # home & dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # quiz management
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/attempt/<int:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),

    # resource features
    path('resource/create/', views.create_resource, name='create'),
    path('search/', views.search_resources, name='search'),
    path('upload/', views.upload_view, name='upload'),

    # library & sessions pages
    path('library/', views.library, name='library'),
    path('sessions/', views.sessions, name='sessions'),

    # other pages (analytics still reachable by URL but not nav)
    path('analytics/', views.analytics, name='analytics'),
    path('students/', views.students, name='students'),
    path('classes/<int:class_id>/', views.classroom_detail, name='classroom_detail'),
    path('class/<int:class_id>/delete/', views.delete_class, name='delete_class'),
    path('upgrade/', views.upgrade, name='upgrade'),
    
    # import integrations
    path('import/google-classroom/', views.import_google_classroom, name='import_google_classroom'),
    path('import/microsoft-teams/', views.import_microsoft_teams, name='import_microsoft_teams'),
]
