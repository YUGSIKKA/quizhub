# Generated manually to add time tracking fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='attempt',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]
