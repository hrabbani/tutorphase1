# Generated by Django 3.1.7 on 2021-06-19 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0009_auto_20210602_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='answer3',
        ),
        migrations.RemoveField(
            model_name='student',
            name='question3',
        ),
    ]
