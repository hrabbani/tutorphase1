# Generated by Django 3.1.7 on 2021-06-20 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0025_auto_20210620_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='note',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
