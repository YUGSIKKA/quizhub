from django.shortcuts import render, get_object_or_404
from .models import Attempt
from quizzes.models import Quiz

def result_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = Attempt.objects.filter(
        user=request.user,
        quiz=quiz
    ).last()

    return render(request, 'results/result.html', {
        'attempt': attempt
    })


def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz).order_by('-percentage')

    return render(request, 'results/leaderboard.html', {
        'attempts': attempts
    })