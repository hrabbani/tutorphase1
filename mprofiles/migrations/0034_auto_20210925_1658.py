# Generated by Django 3.1.7 on 2021-09-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0033_auto_20210831_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('deactivated', 'deactivated')], default='active', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('deactivated', 'deactivated')], default='active', max_length=200, null=True),
        ),
    ]
