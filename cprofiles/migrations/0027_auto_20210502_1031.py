# Generated by Django 3.1.7 on 2021-05-02 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cprofiles', '0026_remove_tasktest_duedate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktest',
            name='tasksubject',
        ),
        migrations.AddField(
            model_name='tasktest',
            name='tasksubject',
            field=models.ManyToManyField(blank=True, related_name='tasksubject', to='cprofiles.Tasksubject'),
        ),
    ]
