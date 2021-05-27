# Generated by Django 3.1.7 on 2021-05-25 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0002_mentor_mentorreason_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='question1',
            field=models.CharField(choices=[('What was the first job you wanted as a kid?', 'What was the first job you wanted as a kid?'), ('If you were one of the seven dwarves in Snow White, which one would you be?', 'If you were one of the seven dwarves in Snow White, which one would you be?'), ('What is your guilty pleasure?', 'What is your guilty pleasure?'), ('What song do you sing in the shower?', 'What song do you sing in the shower?'), ('What is your biggest (non-serious) fear?', 'What is your biggest (non-serious) fear?'), ('What is your favorite binge-watching TV series?', 'What is your favorite binge-watching TV series?'), ('What would your last meal on Earth be?', 'What would your last meal on Earth be?'), ('Who is your favorite person in history?', 'Who is your favorite person in history?'), ('A trip you most want to take but haven’t yet?', 'A trip you most want to take but haven’t yet?')], max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='question2',
            field=models.CharField(choices=[('What was the first job you wanted as a kid?', 'What was the first job you wanted as a kid?'), ('If you were one of the seven dwarves in Snow White, which one would you be?', 'If you were one of the seven dwarves in Snow White, which one would you be?'), ('What is your guilty pleasure?', 'What is your guilty pleasure?'), ('What song do you sing in the shower?', 'What song do you sing in the shower?'), ('What is your biggest (non-serious) fear?', 'What is your biggest (non-serious) fear?'), ('What is your favorite binge-watching TV series?', 'What is your favorite binge-watching TV series?'), ('What would your last meal on Earth be?', 'What would your last meal on Earth be?'), ('Who is your favorite person in history?', 'Who is your favorite person in history?'), ('A trip you most want to take but haven’t yet?', 'A trip you most want to take but haven’t yet?')], max_length=200),
        ),
        migrations.AlterField(
            model_name='student',
            name='question3',
            field=models.CharField(choices=[('What was the first job you wanted as a kid?', 'What was the first job you wanted as a kid?'), ('If you were one of the seven dwarves in Snow White, which one would you be?', 'If you were one of the seven dwarves in Snow White, which one would you be?'), ('What is your guilty pleasure?', 'What is your guilty pleasure?'), ('What song do you sing in the shower?', 'What song do you sing in the shower?'), ('What is your biggest (non-serious) fear?', 'What is your biggest (non-serious) fear?'), ('What is your favorite binge-watching TV series?', 'What is your favorite binge-watching TV series?'), ('What would your last meal on Earth be?', 'What would your last meal on Earth be?'), ('Who is your favorite person in history?', 'Who is your favorite person in history?'), ('A trip you most want to take but haven’t yet?', 'A trip you most want to take but haven’t yet?')], max_length=200),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('inactive', 'inactive'), ('connected', 'connected'), ('disconnected', 'disconnected')], max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('flag', models.BooleanField(default=False)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to='mprofiles.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='mprofiles.student')),
            ],
        ),
    ]
