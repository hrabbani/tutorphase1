# Generated by Django 3.1.7 on 2021-06-15 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0060_auto_20210614_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Academicadvisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200)),
            ],
        ),
    ]