# Generated by Django 3.1.7 on 2021-06-17 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0049_auto_20210617_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='address',
        ),
    ]
