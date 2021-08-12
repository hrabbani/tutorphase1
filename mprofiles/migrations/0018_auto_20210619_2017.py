# Generated by Django 3.1.7 on 2021-06-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0017_auto_20210619_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='available',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='commit',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='seminar',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True),
        ),
    ]