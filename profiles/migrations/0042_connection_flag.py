# Generated by Django 3.1.7 on 2021-05-23 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0041_auto_20210517_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]