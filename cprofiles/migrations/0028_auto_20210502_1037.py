# Generated by Django 3.1.7 on 2021-05-02 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0027_auto_20210502_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktest',
            name='task10status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task1status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task2status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task3status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task4status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task5status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task6status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task7status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task8status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasktest',
            name='task9status',
            field=models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True),
        ),
    ]
