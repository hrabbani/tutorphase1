# Generated by Django 3.1.7 on 2021-06-20 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0024_mentor_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='note',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]