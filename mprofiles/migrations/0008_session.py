# Generated by Django 3.1.7 on 2021-05-26 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0007_delete_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet', models.IntegerField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=1000, null=True)),
                ('help', models.TextField(blank=True, max_length=1000, null=True)),
                ('change', models.TextField(blank=True, max_length=1000, null=True)),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('question', models.TextField(blank=True, max_length=1000, null=True)),
                ('cont', models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=200, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('submit_status', models.BooleanField(default=False)),
                ('flag', models.BooleanField(default=False)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mprofiles.connection')),
                ('support', models.ManyToManyField(blank=True, related_name='sessionsupports', to='mprofiles.Sessionsupport')),
            ],
        ),
    ]
