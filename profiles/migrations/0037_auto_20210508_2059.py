# Generated by Django 3.1.7 on 2021-05-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0036_auto_20210508_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Spanish', 'Spanish')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='student_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
