# Generated by Django 3.1.7 on 2021-04-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0003_auto_20210429_2141'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Csprofile',
            new_name='Student',
        ),
        migrations.AlterField(
            model_name='mentor',
            name='prefer_grade',
            field=models.CharField(choices=[('5', '5'), ('8', '8'), ('no preference', 'no preference')], max_length=200),
        ),
    ]
