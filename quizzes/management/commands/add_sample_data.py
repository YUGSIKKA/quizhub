from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quizzes.models import Quiz, Question, ClassRoom, Student, Resource


class Command(BaseCommand):
    help = 'Add sample data: classrooms, students, quizzes, questions, and resources'

    def handle(self, *args, **options):
        # Delete all existing data first
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        Question.objects.all().delete()
        Quiz.objects.all().delete()
        Student.objects.all().delete()
        ClassRoom.objects.all().delete()
        Resource.objects.all().delete()
        
        # Delete default users (optional - keep admin)
        User.objects.filter(username='teacher').delete()
        User.objects.filter(username='student').delete()
        self.stdout.write(self.style.SUCCESS('Existing data deleted!'))

        # Create teacher user
        teacher = User.objects.create_user(
            username='teacher',
            email='teacher@school.com',
            password='teacher123',
            first_name='John',
            last_name='Teacher'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teacher user: {teacher.username}'))

        # Create student user
        student = User.objects.create_user(
            username='student',
            email='student@school.com',
            password='student123',
            first_name='Jane',
            last_name='Student'
        )
        self.stdout.write(self.style.SUCCESS(f'Created student user: {student.username}'))

        # Create sample classrooms
        classrooms_data = [
            {
                'name': 'Grade 6 - Class A',
                'description': 'Mathematics and Science for Grade 6 students'
            },
            {
                'name': 'Grade 7 - Class B',
                'description': 'Mathematics and Science for Grade 7 students'
            },
            {
                'name': 'Grade 8 - Class A',
                'description': 'Mathematics, Science and English for Grade 8 students'
            },
            {
                'name': 'Grade 9 - Class A',
                'description': 'Advanced Science and Mathematics for Grade 9'
            },
            {
                'name': 'Grade 10 - Class A',
                'description': 'College Preparatory Mathematics and Science'
            },
        ]

        created_classrooms = []
        for classroom_data in classrooms_data:
            classroom = ClassRoom.objects.create(
                name=classroom_data['name'],
                teacher=teacher,
                description=classroom_data['description']
            )
            created_classrooms.append(classroom)
            self.stdout.write(self.style.SUCCESS(f'Created classroom: {classroom.name}'))

        # Create sample students for each classroom
        student_names = [
            'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 
            'Edward Norton', 'Fiona Apple', 'George Washington', 'Hannah Montana',
            'Ian Malcolm', 'Julia Roberts', 'Kevin Hart', 'Liam Nelson',
            'Monica Bellucci', 'Nathan Drake', 'Olivia Wilde', 'Peter Parker'
        ]

        for classroom in created_classrooms:
            for i, name in enumerate(student_names):
                Student.objects.create(
                    classroom=classroom,
                    email=f'{name.lower().replace(" ", ".")}@{classroom.name.lower().replace(" ", "").replace("-", "")}.school.com',
                    defaults={'name': name}
                )
            self.stdout.write(self.style.SUCCESS(f'Created {len(student_names)} students for {classroom.name}'))

        # Create sample quizzes with questions
        quizzes_data = [
            {
                'title': 'Mathematics Basics',
                'description': 'Test your basic math skills',
                'subject': 'Mathematics',
                'grade': 'Grade 6',
                'time_limit': 15,
                'classroom': created_classrooms[0],
                'questions': [
                    {'text': 'What is 12 + 7?', 'option1': '17', 'option2': '19', 'option3': '18', 'option4': '20', 'correct_option': 2},
                    {'text': 'What is 15 x 4?', 'option1': '50', 'option2': '60', 'option3': '55', 'option4': '65', 'correct_option': 2},
                    {'text': 'What is 100 / 4?', 'option1': '20', 'option2': '25', 'option3': '30', 'option4': '35', 'correct_option': 2},
                    {'text': 'What is 8 squared?', 'option1': '64', 'option2': '54', 'option3': '72', 'option4': '56', 'correct_option': 1},
                    {'text': 'What is the square root of 144?', 'option1': '10', 'option2': '11', 'option3': '12', 'option4': '13', 'correct_option': 3},
                    {'text': 'What is 25 + 37?', 'option1': '52', 'option2': '62', 'option3': '72', 'option4': '42', 'correct_option': 2},
                    {'text': 'What is 48 / 6?', 'option1': '6', 'option2': '8', 'option3': '7', 'option4': '9', 'correct_option': 2},
                    {'text': 'What is 9 x 11?', 'option1': '99', 'option2': '89', 'option3': '109', 'option4': '79', 'correct_option': 1},
                ]
            },
            {
                'title': 'Science Quiz: Solar System',
                'description': 'Questions about planets and space',
                'subject': 'Science',
                'grade': 'Grade 6',
                'time_limit': 20,
                'classroom': created_classrooms[0],
                'questions': [
                    {'text': 'Which planet is closest to the Sun?', 'option1': 'Venus', 'option2': 'Mercury', 'option3': 'Mars', 'option4': 'Earth', 'correct_option': 2},
                    {'text': 'Which planet is known as the Red Planet?', 'option1': 'Venus', 'option2': 'Mars', 'option3': 'Jupiter', 'option4': 'Saturn', 'correct_option': 2},
                    {'text': 'How many planets are in our solar system?', 'option1': '7', 'option2': '8', 'option3': '9', 'option4': '10', 'correct_option': 2},
                    {'text': 'Which planet has the most moons?', 'option1': 'Jupiter', 'option2': 'Saturn', 'option3': 'Uranus', 'option4': 'Neptune', 'correct_option': 2},
                    {'text': 'What is the largest planet in our solar system?', 'option1': 'Saturn', 'option2': 'Neptune', 'option3': 'Jupiter', 'option4': 'Uranus', 'correct_option': 3},
                    {'text': 'Which planet is known as the Blue Planet?', 'option1': 'Mars', 'option2': 'Neptune', 'option3': 'Earth', 'option4': 'Uranus', 'correct_option': 3},
                    {'text': 'What is the Sun?', 'option1': 'A planet', 'option2': 'A star', 'option3': 'A moon', 'option4': 'An asteroid', 'correct_option': 2},
                    {'text': 'How long does it take for Earth to orbit the Sun?', 'option1': '365 days', 'option2': '30 days', 'option3': '24 hours', 'option4': '7 days', 'correct_option': 1},
                ]
            },
            {
                'title': 'English Grammar Test',
                'description': 'Test your English grammar knowledge',
                'subject': 'English',
                'grade': 'Grade 7',
                'time_limit': 10,
                'classroom': created_classrooms[1],
                'questions': [
                    {'text': 'Which sentence is correct?', 'option1': 'She go to school', 'option2': 'She goes to school', 'option3': 'She going to school', 'option4': 'She gone to school', 'correct_option': 2},
                    {'text': 'What is the past tense of "go"?', 'option1': 'Goes', 'option2': 'Going', 'option3': 'Went', 'option4': 'Gone', 'correct_option': 3},
                    {'text': 'Which is a noun?', 'option1': 'Run', 'option2': 'Beautiful', 'option3': 'Happiness', 'option4': 'Quickly', 'correct_option': 3},
                    {'text': 'What is the plural of "child"?', 'option1': 'Childs', 'option2': 'Children', 'option3': 'Childes', 'option4': 'Childrens', 'correct_option': 2},
                    {'text': 'Which is a verb?', 'option1': 'Happy', 'option2': 'Quick', 'option3': 'Dance', 'option4': 'Beautiful', 'correct_option': 3},
                    {'text': 'What is an adjective?', 'option1': 'Action word', 'option2': 'Describes a noun', 'option3': 'Connects words', 'option4': 'Shows action', 'correct_option': 2},
                    {'text': 'Which is a pronoun?', 'option1': 'Run', 'option2': 'Beautiful', 'option3': 'He', 'option4': 'Quickly', 'correct_option': 3},
                ]
            },
            {
                'title': 'History: World Wars',
                'description': 'Questions about World War I and II',
                'subject': 'History',
                'grade': 'Grade 8',
                'time_limit': 25,
                'classroom': created_classrooms[2],
                'questions': [
                    {'text': 'In what year did World War I begin?', 'option1': '1912', 'option2': '1914', 'option3': '1916', 'option4': '1918', 'correct_option': 2},
                    {'text': 'In what year did World War II end?', 'option1': '1943', 'option2': '1944', 'option3': '1945', 'option4': '1946', 'correct_option': 3},
                    {'text': 'Who was the leader of Nazi Germany?', 'option1': 'Benito Mussolini', 'option2': 'Joseph Stalin', 'option3': 'Adolf Hitler', 'option4': 'Winston Churchill', 'correct_option': 3},
                    {'text': 'What was the name of the alliance between Germany, Italy, and Japan?', 'option1': 'United Nations', 'option2': 'NATO', 'option3': 'Axis Powers', 'option4': 'Allied Powers', 'correct_option': 3},
                    {'text': 'Where was the D-Day invasion (Normandy) located?', 'option1': 'France', 'option2': 'Germany', 'option3': 'Italy', 'option4': 'Belgium', 'correct_option': 1},
                    {'text': 'What event triggered World War I?', 'option1': 'Attack on Pearl Harbor', 'option2': 'Assassination of Archduke Franz Ferdinand', 'option3': 'Invasion of Poland', 'option4': 'Russian Revolution', 'correct_option': 2},
                ]
            },
            {
                'title': 'Geography: Countries and Capitals',
                'description': 'Test your knowledge of world capitals',
                'subject': 'Geography',
                'grade': 'Grade 7',
                'time_limit': 15,
                'classroom': created_classrooms[1],
                'questions': [
                    {'text': 'What is the capital of France?', 'option1': 'London', 'option2': 'Paris', 'option3': 'Berlin', 'option4': 'Madrid', 'correct_option': 2},
                    {'text': 'What is the capital of Japan?', 'option1': 'Seoul', 'option2': 'Beijing', 'option3': 'Tokyo', 'option4': 'Bangkok', 'correct_option': 3},
                    {'text': 'What is the capital of Australia?', 'option1': 'Sydney', 'option2': 'Melbourne', 'option3': 'Canberra', 'option4': 'Perth', 'correct_option': 3},
                    {'text': 'What is the capital of Brazil?', 'option1': 'Rio de Janeiro', 'option2': 'São Paulo', 'option3': 'Brasília', 'option4': 'Salvador', 'correct_option': 3},
                    {'text': 'What is the capital of Canada?', 'option1': 'Toronto', 'option2': 'Vancouver', 'option3': 'Ottawa', 'option4': 'Montreal', 'correct_option': 3},
                    {'text': 'What is the capital of India?', 'option1': 'Mumbai', 'option2': 'Kolkata', 'option3': 'New Delhi', 'option4': 'Chennai', 'correct_option': 3},
                    {'text': 'What is the capital of Germany?', 'option1': 'Munich', 'option2': 'Hamburg', 'option3': 'Berlin', 'option4': 'Frankfurt', 'correct_option': 3},
                ]
            },
            {
                'title': 'Physics: Motion and Forces',
                'description': 'Basic physics concepts about motion',
                'subject': 'Physics',
                'grade': 'Grade 9',
                'time_limit': 20,
                'classroom': created_classrooms[3],
                'questions': [
                    {'text': 'What is the formula for speed?', 'option1': 'Distance / Time', 'option2': 'Distance x Time', 'option3': 'Time / Distance', 'option4': 'Distance + Time', 'correct_option': 1},
                    {'text': 'What is Newton\'s first law also known as?', 'option1': 'Law of Gravity', 'option2': 'Law of Inertia', 'option3': 'Law of Conservation', 'option4': 'Law of Momentum', 'correct_option': 2},
                    {'text': 'What is the unit of force?', 'option1': 'Joule', 'option2': 'Watt', 'option3': 'Newton', 'option4': 'Pascal', 'correct_option': 3},
                    {'text': 'What is acceleration?', 'option1': 'Change in velocity', 'option2': 'Change in mass', 'option3': 'Change in time', 'option4': 'Change in distance', 'correct_option': 1},
                    {'text': 'What keeps planets in orbit around the Sun?', 'option1': 'Magnetic force', 'option2': 'Gravity', 'option3': 'Electric force', 'option4': 'Nuclear force', 'correct_option': 2},
                ]
            },
            {
                'title': 'Chemistry: Elements and Compounds',
                'description': 'Introduction to chemistry',
                'subject': 'Chemistry',
                'grade': 'Grade 9',
                'time_limit': 20,
                'classroom': created_classrooms[3],
                'questions': [
                    {'text': 'What is the chemical symbol for water?', 'option1': 'H2O', 'option2': 'CO2', 'option3': 'NaCl', 'option4': 'O2', 'correct_option': 1},
                    {'text': 'What is the atomic number of Carbon?', 'option1': '4', 'option2': '6', 'option3': '8', 'option4': '12', 'correct_option': 2},
                    {'text': 'What is a molecule?', 'option1': 'Single atom', 'option2': 'Two or more atoms bonded', 'option3': 'A compound only', 'option4': 'A mixture', 'correct_option': 2},
                    {'text': 'What is the periodic table?', 'option1': 'A list of planets', 'option2': 'Organization of elements', 'option3': 'A math table', 'option4': 'A map', 'correct_option': 2},
                    {'text': 'What is a noble gas?', 'option1': 'Reactive gases', 'option2': 'Unreactive gases', 'option3': 'Heavy gases', 'option4': 'Light gases', 'correct_option': 2},
                ]
            },
            {
                'title': 'Biology: Cell Structure',
                'description': 'Learn about cells',
                'subject': 'Biology',
                'grade': 'Grade 10',
                'time_limit': 20,
                'classroom': created_classrooms[4],
                'questions': [
                    {'text': 'What is the powerhouse of the cell?', 'option1': 'Nucleus', 'option2': 'Ribosome', 'option3': 'Mitochondria', 'option4': 'Cell membrane', 'correct_option': 3},
                    {'text': 'What is the function of the nucleus?', 'option1': 'Energy production', 'option2': 'Contains DNA', 'option3': 'Protein synthesis', 'option4': 'Cell division', 'correct_option': 2},
                    {'text': 'What is photosynthesis?', 'option1': 'Cell respiration', 'option2': 'Making food from sunlight', 'option3': 'Cell division', 'option4': 'Waste removal', 'correct_option': 2},
                    {'text': 'What is DNA?', 'option1': 'Cell structure', 'option2': 'Genetic material', 'option3': 'Cell membrane', 'option4': 'Energy', 'correct_option': 2},
                    {'text': 'What is the cell membrane made of?', 'option1': 'Protein only', 'option2': 'Lipids and proteins', 'option3': 'Carbohydrates only', 'option4': 'DNA only', 'correct_option': 2},
                ]
            },
        ]

        total_questions = 0
        for quiz_data in quizzes_data:
            classroom = quiz_data.pop('classroom')
            questions = quiz_data.pop('questions')
            
            quiz = Quiz.objects.create(
                title=quiz_data['title'],
                description=quiz_data['description'],
                subject=quiz_data['subject'],
                grade=quiz_data['grade'],
                time_limit=quiz_data['time_limit'],
                created_by=teacher
            )
            quiz.classroom.add(classroom)
            
            for q in questions:
                Question.objects.create(
                    quiz=quiz,
                    text=q['text'],
                    option1=q['option1'],
                    option2=q['option2'],
                    option3=q['option3'],
                    option4=q['option4'],
                    correct_option=q['correct_option']
                )
                total_questions += 1
            
            self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz.title} with {len(questions)} questions'))

        # Create MORE sample resources (varied subjects)
        resources_data = [
            # Mathematics
            {'title': 'Mathematics Formula Sheet Grade 6', 'description': 'Complete formulas for Grade 6 Mathematics including algebra, geometry, and arithmetic', 'subject': 'Mathematics'},
            {'title': 'Algebra Basics Guide', 'description': 'Introduction to algebraic expressions and equations', 'subject': 'Mathematics'},
            {'title': 'Geometry Theorems', 'description': 'Important geometry theorems and proofs', 'subject': 'Mathematics'},
            {'title': 'Math Practice Problems', 'description': '100+ practice problems with solutions', 'subject': 'Mathematics'},
            
            # Science
            {'title': 'Science Vocabulary List', 'description': 'Important science terms and definitions for Grade 6-8', 'subject': 'Science'},
            {'title': 'Solar System Factsheet', 'description': 'Complete guide to planets, moons, and space', 'subject': 'Science'},
            {'title': 'Scientific Method Steps', 'description': 'How to conduct scientific experiments', 'subject': 'Science'},
            {'title': 'Weather and Climate Guide', 'description': 'Understanding weather patterns and climate', 'subject': 'Science'},
            
            # English
            {'title': 'English Grammar Guide', 'description': 'Comprehensive English grammar rules', 'subject': 'English'},
            {'title': 'Vocabulary Building Words', 'description': '500+ important vocabulary words', 'subject': 'English'},
            {'title': 'Essay Writing Tips', 'description': 'How to write perfect essays', 'subject': 'English'},
            {'title': 'Punctuation Rules', 'description': 'Complete guide to English punctuation', 'subject': 'English'},
            
            # History
            {'title': 'World History Timeline', 'description': 'Important events in world history', 'subject': 'History'},
            {'title': 'World War I Summary', 'description': 'Key facts about WWI', 'subject': 'History'},
            {'title': 'World War II Summary', 'description': 'Key facts about WWII', 'subject': 'History'},
            {'title': 'Ancient Civilizations', 'description': 'Egypt, Greece, Rome and more', 'subject': 'History'},
            
            # Geography
            {'title': 'World Atlas', 'description': 'Maps of all continents and countries', 'subject': 'Geography'},
            {'title': 'Country Capitals List', 'description': 'Capital cities of 200+ countries', 'subject': 'Geography'},
            {'title': 'Climate Zones Guide', 'description': 'Understanding different climate types', 'subject': 'Geography'},
            {'title': 'Natural Disasters', 'description': 'Types and causes of natural disasters', 'subject': 'Geography'},
            
            # Physics
            {'title': 'Physics Formulas', 'description': 'All important physics formulas', 'subject': 'Physics'},
            {'title': 'Motion and Forces Notes', 'description': 'Understanding motion, velocity, and acceleration', 'subject': 'Physics'},
            {'title': 'Energy and Work', 'description': 'Guide to energy concepts', 'subject': 'Physics'},
            
            # Chemistry
            {'title': 'Periodic Table Guide', 'description': 'Complete periodic table with element details', 'subject': 'Chemistry'},
            {'title': 'Chemical Reactions', 'description': 'Types of chemical reactions', 'subject': 'Chemistry'},
            {'title': 'Acids and Bases', 'description': 'Understanding acids, bases, and pH', 'subject': 'Chemistry'},
            
            # Biology
            {'title': 'Cell Biology Guide', 'description': 'Complete cell structure and function', 'subject': 'Biology'},
            {'title': 'Human Body Systems', 'description': 'Digestive, circulatory, nervous system and more', 'subject': 'Biology'},
            {'title': 'Genetics Basics', 'description': 'Introduction to heredity and DNA', 'subject': 'Biology'},
            {'title': 'Ecosystems and Food Chains', 'description': 'Understanding ecological systems', 'subject': 'Biology'},
        ]

        for resource_data in resources_data:
            Resource.objects.create(
                title=resource_data['title'],
                description=resource_data['description'],
                subject=resource_data['subject'],
                created_by=teacher
            )

        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Summary ==='))
        self.stdout.write(f'Users: {User.objects.count()} (1 teacher, 1 student)')
        self.stdout.write(f'Classrooms: {ClassRoom.objects.count()}')
        self.stdout.write(f'Students: {Student.objects.count()}')
        self.stdout.write(f'Quizzes: {Quiz.objects.count()}')
        self.stdout.write(f'Questions: {total_questions}')
        self.stdout.write(f'Resources: {Resource.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n=== Login Credentials ==='))
        self.stdout.write(f'Teacher: username=teacher, password=teacher123')
        self.stdout.write(f'Student: username=student, password=student123')
        self.stdout.write(self.style.SUCCESS('\nDone! Sample data has been added successfully!'))
