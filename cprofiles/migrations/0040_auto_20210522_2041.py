# Generated by Django 3.1.7 on 2021-05-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0039_auto_20210522_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
