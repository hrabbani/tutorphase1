# Generated by Django 3.1.7 on 2021-04-19 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20210418_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('tutor', 'tutor'), ('student', 'student')], max_length=200, null=True)),
                ('avatar', models.ImageField(default='avatar.png', upload_to='avatars/')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('school', models.CharField(blank=True, max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='_testprofile_friends_+', to='profiles.TestProfile')),
                ('subjects', models.ManyToManyField(blank=True, related_name='testsubjects', to='profiles.Subject')),
            ],
        ),
    ]
