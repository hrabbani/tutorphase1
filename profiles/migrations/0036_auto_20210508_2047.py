# Generated by Django 3.1.7 on 2021-05-08 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0035_auto_20210505_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='parent1_email',
            field=models.EmailField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent1_first_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent1_last_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent1_phone',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent2_email',
            field=models.EmailField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent2_first_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent2_last_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='parent2_phone',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
