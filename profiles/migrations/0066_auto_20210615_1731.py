# Generated by Django 3.1.7 on 2021-06-15 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0065_auto_20210615_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='academic_advisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='academic_advisor', to='profiles.academicadvisor'),
        ),
    ]