# Generated by Django 3.1.7 on 2021-04-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0028_auto_20210423_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]