# Generated by Django 3.1.7 on 2021-08-02 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0067_student_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='note',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
