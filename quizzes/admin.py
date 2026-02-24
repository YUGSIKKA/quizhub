from django.contrib import admin
from .models import Quiz, ClassRoom, Student, Question, Resource, Option

# Register all models
admin.site.register(Quiz)
admin.site.register(ClassRoom)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Resource)
admin.site.register(Option)
