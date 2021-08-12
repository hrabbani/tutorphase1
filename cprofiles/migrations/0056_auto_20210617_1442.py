# Generated by Django 3.1.7 on 2021-06-17 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0055_auto_20210617_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentorlanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='mentor',
            name='experience',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='language',
        ),
        migrations.AlterField(
            model_name='mentor',
            name='mentor_last_year',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='prefer_location',
            field=models.ManyToManyField(blank=True, related_name='prefer_location', to='cprofiles.Preferlocation'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='language',
            field=models.ManyToManyField(blank=True, related_name='mentor_language', to='cprofiles.Mentorlanguage'),
        ),
    ]