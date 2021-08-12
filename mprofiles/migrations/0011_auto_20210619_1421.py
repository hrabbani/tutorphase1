# Generated by Django 3.1.7 on 2021-06-19 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0010_auto_20210619_1413'),
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
        migrations.AlterField(
            model_name='student',
            name='academic_advisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic_advisor', to='mprofiles.academicadvisor'),
        ),
    ]