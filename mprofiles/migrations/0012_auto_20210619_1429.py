# Generated by Django 3.1.7 on 2021-06-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0011_auto_20210619_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='reason',
        ),
        migrations.AddField(
            model_name='student',
            name='reason',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='Reason',
        ),
    ]
