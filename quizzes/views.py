from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Quiz, Question, Option, ClassRoom, Student, Resource
from .forms import QuizForm, QuestionForm, ClassRoomForm, StudentForm, ResourceForm
from results.models import Attempt
from accounts.decorators import teacher_required, student_required



def home(request):
    # Always show landing page at root URL
    # Users can navigate to dashboard via the button on the landing page
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    from django.db.models import Avg, Count
    quizzes = Quiz.objects.all().order_by('-id')[:20]
    
    # Get real statistics
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    total_attempts = Attempt.objects.count()
    
    # Calculate average score
    avg_score = 0
    if total_attempts > 0:
        avg_score = Attempt.objects.aggregate(avg=Avg('percentage'))['avg'] or 0
    
    # Get unique subjects for filter pills
    subjects = Quiz.objects.values_list('subject', flat=True).distinct()
    
    # Get user's recent attempts
    user_attempts = Attempt.objects.filter(user=request.user).order_by('-id')[:5] if request.user.is_authenticated else []
    
    # Get average time taken
    avg_time = Attempt.objects.aggregate(avg_time=Avg('time_taken'))['avg_time'] or 0
    
    return render(request, 'quizzes/dashboard.html', {
        'quizzes': quizzes,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'subjects': subjects,
        'user_attempts': user_attempts,
        'avg_time': round(avg_time, 0)
    })

def analytics(request):
    from .models import Quiz, Question
    from results.models import Attempt
    from django.db.models import Avg, Count
    
    # Get all quizzes and questions
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    
    # Get all attempts
    total_attempts = Attempt.objects.count()
    
    # Calculate average score
    avg_score = 0
    if total_attempts > 0:
        avg_result = Attempt.objects.aggregate(avg=Avg('percentage'))
        avg_score = round(avg_result['avg'] or 0, 1)
    
    # Performance breakdown
    excellent_count = Attempt.objects.filter(percentage__gte=70).count()
    good_count = Attempt.objects.filter(percentage__gte=40, percentage__lt=70).count()
    needs_improvement_count = Attempt.objects.filter(percentage__lt=40).count()
    
    # Subject distribution - count quizzes per subject
    subject_data = Quiz.objects.values('subject').annotate(count=Count('id')).order_by('-count')
    subject_labels = [item['subject'] for item in subject_data]
    subject_counts = [item['count'] for item in subject_data]
    
    # Recent attempts with user and quiz info
    recent_attempts = Attempt.objects.select_related('user', 'quiz').order_by('-id')[:10]
    
    context = {
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'excellent_count': excellent_count,
        'good_count': good_count,
        'needs_improvement_count': needs_improvement_count,
        'subject_labels': subject_labels,
        'subject_counts': subject_counts,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'quizzes/analytics.html', context)

@login_required
def sessions(request):
    from django.db.models import Avg
    from results.models import Attempt
    
    query = request.GET.get('q', '').strip()
    subject_filter = request.GET.get('subject', '').strip()
    grade_filter = request.GET.get('grade', '').strip()
    
    # Get user's attempted quiz IDs
    user_attempted_quiz_ids = Attempt.objects.filter(user=request.user).values_list('quiz_id', flat=True).distinct()
    
    # Get quizzes user has attempted (not just created)
    quizzes = Quiz.objects.filter(
        Q(created_by=request.user) | Q(id__in=user_attempted_quiz_ids)
    ).distinct().prefetch_related('question_set')
    
    if query:
        quizzes = quizzes.filter(title__icontains=query)
    if subject_filter:
        quizzes = quizzes.filter(subject__icontains=subject_filter)
    if grade_filter:
        quizzes = quizzes.filter(grade__icontains=grade_filter)
    
    # Get statistics - include all attempted quizzes
    total_quizzes = Quiz.objects.filter(
        Q(created_by=request.user) | Q(id__in=user_attempted_quiz_ids)
    ).distinct().count()
    
    # Get all attempts by user
    user_attempts = Attempt.objects.filter(user=request.user)
    total_attempts = user_attempts.count()
    
    avg_score = 0
    if total_attempts > 0:
        avg_score = user_attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
    
    # Get unique subjects and grades for filters
    subjects = Quiz.objects.filter(
        Q(created_by=request.user) | Q(id__in=user_attempted_quiz_ids)
    ).distinct().values_list('subject', flat=True).distinct()
    grades = Quiz.objects.filter(
        Q(created_by=request.user) | Q(id__in=user_attempted_quiz_ids)
    ).distinct().values_list('grade', flat=True).distinct()
    
    # Get recent attempts for activity (all attempts by user)
    recent_attempts = user_attempts.select_related('quiz').order_by('-id')[:10]
    
    # Add stats to each quiz
    quiz_data = []
    for quiz in quizzes:
        attempts = Attempt.objects.filter(quiz=quiz)
        attempt_count = attempts.count()
        best_score = attempts.order_by('-percentage').first().percentage if attempt_count > 0 else 0
        user_best = user_attempts.filter(quiz=quiz).order_by('-percentage').first().percentage if user_attempts.filter(quiz=quiz).exists() else 0
        
        quiz_data.append({
            'quiz': quiz,
            'attempt_count': attempt_count,
            'best_score': best_score,
            'user_best': user_best,
            'question_count': quiz.question_set.count()
        })
    
    return render(request, 'quizzes/sessions.html', {
        'quizzes': quizzes,
        'quiz_data': quiz_data,
        'query': query,
        'subject_filter': subject_filter,
        'grade_filter': grade_filter,
        'subjects': subjects,
        'grades': grades,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'recent_attempts': recent_attempts
    })

@login_required
def library(request):
    query = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '').strip()
    
    # Show all resources and quizzes (not just created by current user)
    resources = Resource.objects.all()
    quizzes = Quiz.objects.all()
    
    if query:
        resources = resources.filter(title__icontains=query)
        quizzes = quizzes.filter(title__icontains=query)
    
    # Get statistics - show all resources and quizzes
    total_resources = Resource.objects.count()
    total_quizzes = Quiz.objects.count()
    
    # Get recent items
    recent_resources = Resource.objects.order_by('-created_at')[:5]
    recent_quizzes = Quiz.objects.order_by('-id')[:5]
    
    return render(request, 'quizzes/library.html', {
        'resources': resources,
        'quizzes': quizzes,
        'query': query,
        'type_filter': type_filter,
        'total_resources': total_resources,
        'total_quizzes': total_quizzes,
        'recent_resources': recent_resources,
        'recent_quizzes': recent_quizzes
    })

@login_required
def students(request):
    classes = ClassRoom.objects.filter(teacher=request.user).prefetch_related('students')
    
    # Get statistics
    total_classes = classes.count()
    total_students = sum(c.students.count() for c in classes)

    if request.method == "POST":
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = request.user
            new_class.save()
            return redirect('students')
    else:
        form = ClassRoomForm()

    return render(request, 'quizzes/students.html', {
        'classes': classes,
        'form': form,
        'total_classes': total_classes,
        'total_students': total_students
    })

def upgrade(request):
    return render(request, 'quizzes/upgrade.html')

@login_required
def classroom_detail(request, class_id):
    classroom = get_object_or_404(ClassRoom, id=class_id, teacher=request.user)
    students = classroom.students.all()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('classroom_detail', class_id=classroom.id)
    else:
        form = StudentForm()

    return render(request, 'quizzes/classroom_detail.html', {
        'classroom': classroom,
        'students': students,
        'form': form
    })


@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            
            # Get the number of questions from the form
            num_questions = int(request.POST.get('num_questions', 0))
            
            # Create each question with options
            for i in range(1, num_questions + 1):
                question_text = request.POST.get(f'question_{i}')
                if question_text:
                    option1 = request.POST.get(f'question_{i}_option1')
                    option2 = request.POST.get(f'question_{i}_option2')
                    option3 = request.POST.get(f'question_{i}_option3')
                    option4 = request.POST.get(f'question_{i}_option4')
                    correct_option = request.POST.get(f'question_{i}_correct')
                    
                    # Create the question
                    question = Question.objects.create(
                        quiz=quiz,
                        text=question_text,
                        option1=option1 or "",
                        option2=option2 or "",
                        option3=option3 or "",
                        option4=option4 or "",
                        correct_option=int(correct_option) if correct_option else 1
                    )
            
            return redirect('dashboard')
    else:
        form = QuizForm()
    return render(request, 'quizzes/create_quiz.html', {'form': form})


@login_required
def attempt_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        time_taken = int(request.POST.get('time_taken', 0))

        for question in questions:
            # Get the selected option using the correct key format: question_{id}
            selected = request.POST.get(f'question_{question.id}')
            # Compare with the correct_option integer field (1-4)
            if selected and int(selected) == question.correct_option:
                score += 1

        if total > 0:
            percentage = (score / total) * 100
        else:
            percentage = 0

        Attempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total,
            percentage=percentage,
            time_taken=time_taken
        )

        return redirect('result', quiz_id=quiz.id)
    
    time_limit_value = quiz.time_limit if quiz.time_limit else 10

    return render(request, 'quizzes/attempt_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit': time_limit_value
    })

@login_required
def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            return redirect('dashboard')
    else:
        form = ResourceForm()

    return render(request, 'create.html', {'form': form})


def search_resources(request):
    query = request.GET.get('q', '').strip()

    if query:
        resource_results = Resource.objects.filter(title__icontains=query)
        quiz_results = Quiz.objects.filter(title__icontains=query)
    else:
        resource_results = Resource.objects.none()
        quiz_results = Quiz.objects.none()

    return render(request, 'search.html', {
        'query': query,
        'resource_results': resource_results,
        'quiz_results': quiz_results,
    })


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()
            return redirect('upload')
    else:
        form = ResourceForm()

    resources = Resource.objects.filter(created_by=request.user)
    return render(request, 'upload.html', {'resources': resources, 'form': form})


@login_required
def delete_class(request, class_id):
    """Delete a class and its associated students"""
    classroom = get_object_or_404(ClassRoom, id=class_id, teacher=request.user)
    classroom.delete()
    return redirect('students')


@login_required
def import_google_classroom(request):
    """Import class from Google Classroom"""
    if request.method == 'POST':
        class_name = request.POST.get('class_name', '')
        class_code = request.POST.get('class_code', '')
        
        if class_name:
            # Create a new classroom with Google Classroom indicator
            classroom = ClassRoom.objects.create(
                name=class_name,
                teacher=request.user,
                description=f"Imported from Google Classroom (Code: {class_code})"
            )
            
    return redirect('students')


@login_required
def import_microsoft_teams(request):
    """Import class from Microsoft Teams"""
    if request.method == 'POST':
        team_name = request.POST.get('team_name', '')
        team_id = request.POST.get('team_id', '')
        
        if team_name:
            # Create a new classroom with Microsoft Teams indicator
            classroom = ClassRoom.objects.create(
                name=team_name,
                teacher=request.user,
                description=f"Imported from Microsoft Teams (ID: {team_id})"
            )
            
    return redirect('students')
