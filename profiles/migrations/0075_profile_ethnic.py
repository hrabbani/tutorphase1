# Generated by Django 3.1.7 on 2021-07-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0074_auto_20210705_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ethnic',
            field=models.CharField(blank=True, choices=[('African American or Black', 'African American or Black'), ('American Indian or Alaskan Native', 'American Indian or Alaskan Native'), ('Asian American', 'Asian American'), ('Caucasian or White', 'Caucasian or White'), ('Hispanic or Latino', 'Hispanic or Latino'), ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'), ('I prefer not to say', 'I prefer not to say')], max_length=200, null=True),
        ),
    ]
