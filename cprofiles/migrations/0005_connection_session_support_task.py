# Generated by Django 3.1.7 on 2021-04-30 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0004_auto_20210429_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('inactive', 'inactive'), ('connected', 'connected'), ('disconnected', 'disconnected')], max_length=200)),
                ('progress', models.CharField(choices=[('on track', 'on track'), ('off track', 'off track')], max_length=200)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to='cprofiles.mentor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='cprofiles.student')),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('deadline', models.DateField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('completed', 'completed'), ('not completed', 'not completed')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet', models.IntegerField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.TextField(blank=True, max_length=1000, null=True)),
                ('change', models.TextField(blank=True, max_length=1000, null=True)),
                ('othersupport', models.CharField(blank=True, max_length=200, null=True)),
                ('question', models.TextField(blank=True, max_length=1000, null=True)),
                ('cont', models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True)),
                ('submit_status', models.BooleanField(default=False)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cprofiles.connection')),
                ('support', models.ManyToManyField(blank=True, related_name='supports', to='cprofiles.Support')),
                ('task', models.ManyToManyField(blank=True, related_name='tasks', to='cprofiles.Task')),
            ],
        ),
    ]