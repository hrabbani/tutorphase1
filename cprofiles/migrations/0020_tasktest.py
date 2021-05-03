# Generated by Django 3.1.7 on 2021-05-01 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0019_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(blank=True, max_length=200, null=True)),
                ('duedate', models.DateField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200, null=True)),
                ('connection', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cprofiles.connection')),
                ('student', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cprofiles.student')),
            ],
        ),
    ]
