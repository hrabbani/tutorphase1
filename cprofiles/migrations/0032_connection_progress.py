# Generated by Django 3.1.7 on 2021-05-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0031_auto_20210503_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='progress',
            field=models.CharField(blank=True, choices=[('on track', 'on track'), ('off track', 'off track')], max_length=200, null=True),
        ),
    ]
