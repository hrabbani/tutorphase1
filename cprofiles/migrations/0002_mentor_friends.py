# Generated by Django 3.1.7 on 2021-04-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='csprofile', to='cprofiles.Csprofile'),
        ),
    ]
