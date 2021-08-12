# Generated by Django 3.1.7 on 2021-06-18 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0060_topiccalculation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parentsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meet', models.IntegerField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('share', models.TextField(blank=True, max_length=1000, null=True)),
                ('change', models.TextField(blank=True, max_length=1000, null=True)),
                ('question', models.TextField(blank=True, max_length=1000, null=True)),
                ('submit_status', models.BooleanField(default=False)),
                ('flag', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('connection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cprofiles.connection')),
                ('topic', models.ManyToManyField(blank=True, related_name='parent_topics', to='cprofiles.Topic')),
            ],
        ),
    ]