# Generated by Django 3.1.7 on 2021-05-17 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0040_profile_academic_advisor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
