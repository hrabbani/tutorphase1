# Generated by Django 3.1.7 on 2021-04-20 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_profile_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='middle_name',
        ),
    ]
