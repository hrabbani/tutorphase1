# Generated by Django 3.1.7 on 2021-07-22 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0063_mentor_ethnic'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentsession',
            name='urgent_check',
            field=models.BooleanField(default=False),
        ),
    ]
