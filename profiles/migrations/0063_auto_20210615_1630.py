# Generated by Django 3.1.7 on 2021-06-15 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0062_auto_20210615_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='academic_advisor',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]