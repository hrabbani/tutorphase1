# Generated by Django 3.1.7 on 2021-05-08 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0034_copytask'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='parent_email',
            new_name='parent1_email',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='parent_first_name',
            new_name='parent1_first_name',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='parent_last_name',
            new_name='parent1_last_name',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='parent_phone',
            new_name='parent1_phone',
        ),
    ]
