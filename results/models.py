from django.db import models
from django.contrib.auth.models import User
from quizzes.models import Quiz

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    start_time = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(default=0)  # in seconds
