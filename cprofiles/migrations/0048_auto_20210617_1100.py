# Generated by Django 3.1.7 on 2021-06-17 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0047_auto_20210617_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='parent2_email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parent2_first_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parent2_last_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parent2_phone',
        ),
    ]
