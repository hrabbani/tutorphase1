# Generated by Django 3.1.7 on 2021-09-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0080_auto_20210726_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='student_grade',
            field=models.CharField(blank=True, choices=[('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=200, null=True),
        ),
    ]
