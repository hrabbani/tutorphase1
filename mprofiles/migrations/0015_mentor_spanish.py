# Generated by Django 3.1.7 on 2021-06-19 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0014_auto_20210619_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='spanish',
            field=models.CharField(blank=True, choices=[('Not at all', 'Not at all'), ('Low (can make simple conversation)', 'Low (can make simple conversation)'), ('Medium (somewhat fluent)', 'Medium (somewhat fluent)'), ('High (proficient enough to have a lengthy and detailed conversation)', 'High (proficient enough to have a lengthy and detailed conversation)')], max_length=200, null=True),
        ),
    ]
