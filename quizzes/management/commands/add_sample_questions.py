from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question

class Command(BaseCommand):
    help = 'Add sample MCQ questions to existing quizzes'

    def handle(self, *args, **options):
        quizzes = Quiz.objects.all()
        self.stdout.write(f'Total quizzes: {quizzes.count()}')
        
        for q in quizzes:
            questions = q.question_set.count()
            self.stdout.write(f'Quiz: {q.title} - Questions: {questions}')
            
            # If no questions exist, create sample MCQ questions
            if questions == 0:
                self.stdout.write(f'  Creating sample questions for: {q.title}')
                
                sample_questions = [
                    {
                        'text': 'What is the capital of France?',
                        'option1': 'London',
                        'option2': 'Paris',
                        'option3': 'Berlin',
                        'option4': 'Madrid',
                        'correct_option': 2
                    },
                    {
                        'text': 'Which planet is known as the Red Planet?',
                        'option1': 'Venus',
                        'option2': 'Mars',
                        'option3': 'Jupiter',
                        'option4': 'Saturn',
                        'correct_option': 2
                    },
                    {
                        'text': 'What is 5 + 3?',
                        'option1': '7',
                        'option2': '9',
                        'option3': '8',
                        'option4': '10',
                        'correct_option': 3
                    },
                    {
                        'text': 'Who wrote "Romeo and Juliet"?',
                        'option1': 'Charles Dickens',
                        'option2': 'William Shakespeare',
                        'option3': 'Jane Austen',
                        'option4': 'Mark Twain',
                        'correct_option': 2
                    },
                    {
                        'text': 'What is the largest mammal in the world?',
                        'option1': 'Elephant',
                        'option2': 'Blue Whale',
                        'option3': 'Giraffe',
                        'option4': 'Hippopotamus',
                        'correct_option': 2
                    }
                ]
                
                for sq in sample_questions:
                    Question.objects.create(
                        quiz=q,
                        text=sq['text'],
                        option1=sq['option1'],
                        option2=sq['option2'],
                        option3=sq['option3'],
                        option4=sq['option4'],
                        correct_option=sq['correct_option']
                    )
                self.stdout.write(self.style.SUCCESS(f'  Created {len(sample_questions)} questions!'))
        
        self.stdout.write(self.style.SUCCESS('\nDone!'))
