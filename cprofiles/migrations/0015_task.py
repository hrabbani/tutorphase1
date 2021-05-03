# Generated by Django 3.1.7 on 2021-05-01 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0014_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task1', models.CharField(blank=True, max_length=200, null=True)),
                ('task2', models.CharField(blank=True, max_length=200, null=True)),
                ('task3', models.CharField(blank=True, max_length=200, null=True)),
                ('task4', models.CharField(blank=True, max_length=200, null=True)),
                ('task5', models.CharField(blank=True, max_length=200, null=True)),
                ('task6', models.CharField(blank=True, max_length=200, null=True)),
                ('task7', models.CharField(blank=True, max_length=200, null=True)),
                ('task8', models.CharField(blank=True, max_length=200, null=True)),
                ('task9', models.CharField(blank=True, max_length=200, null=True)),
                ('task10', models.CharField(blank=True, max_length=200, null=True)),
                ('tast1date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast2date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast3date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast4date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast5date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast6date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast7date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast8date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast9date', models.DateField(blank=True, max_length=200, null=True)),
                ('tast10date', models.DateField(blank=True, max_length=200, null=True)),
                ('task1status', models.CharField(blank=True, max_length=200, null=True)),
                ('task2status', models.CharField(blank=True, max_length=200, null=True)),
                ('task3status', models.CharField(blank=True, max_length=200, null=True)),
                ('task4status', models.CharField(blank=True, max_length=200, null=True)),
                ('task5status', models.CharField(blank=True, max_length=200, null=True)),
                ('task6status', models.CharField(blank=True, max_length=200, null=True)),
                ('task7status', models.CharField(blank=True, max_length=200, null=True)),
                ('task8status', models.CharField(blank=True, max_length=200, null=True)),
                ('task9status', models.CharField(blank=True, max_length=200, null=True)),
                ('task10status', models.CharField(blank=True, max_length=200, null=True)),
                ('connection', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cprofiles.connection')),
                ('student', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cprofiles.student')),
            ],
        ),
    ]
