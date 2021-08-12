# Generated by Django 3.1.7 on 2021-06-17 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0048_auto_20210617_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Childstrength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Socialstrength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='student',
            old_name='parent_response',
            new_name='dont_know',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='prompt',
            new_name='happy',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='reason',
            new_name='int_ind_school',
        ),
        migrations.AddField(
            model_name='student',
            name='ind_scl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='learn',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='look_ind_school',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='obstacle',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='proud',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='strength',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='child_strength',
            field=models.ManyToManyField(blank=True, related_name='child_strength', to='cprofiles.Childstrength'),
        ),
        migrations.AddField(
            model_name='student',
            name='social_strength',
            field=models.ManyToManyField(blank=True, related_name='social_strength', to='cprofiles.Socialstrength'),
        ),
    ]