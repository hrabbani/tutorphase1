# Generated by Django 3.1.7 on 2021-05-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0040_auto_20210522_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('connected', 'connected'), ('disconnected', 'disconnected'), ('off track', 'off track')], max_length=200),
        ),
    ]
