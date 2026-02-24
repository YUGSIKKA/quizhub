# Generated manually to add time_limit back

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='time_limit',
            field=models.IntegerField(default=10, help_text='Time limit in minutes'),
        ),
    ]
