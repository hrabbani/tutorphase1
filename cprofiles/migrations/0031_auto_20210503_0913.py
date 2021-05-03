# Generated by Django 3.1.7 on 2021-05-03 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0030_auto_20210502_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='session',
            name='othersupport',
        ),
        migrations.AddField(
            model_name='session',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='topic',
            field=models.ManyToManyField(blank=True, related_name='topics', to='cprofiles.Topic'),
        ),
    ]
