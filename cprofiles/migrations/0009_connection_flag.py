# Generated by Django 3.1.7 on 2021-04-30 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0008_student_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]