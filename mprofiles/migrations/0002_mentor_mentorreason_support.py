# Generated by Django 3.1.7 on 2021-05-24 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentorreason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
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
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='avatar.png', upload_to='avatars/')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('language', models.TextField(blank=True, max_length=1000, null=True)),
                ('emergency_contact', models.TextField(blank=True, max_length=1000, null=True)),
                ('employment_status', models.CharField(choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Unemployed', 'Unemployed'), ('Retired', 'Retired')], max_length=200)),
                ('employer_info', models.TextField(blank=True, max_length=1000, null=True)),
                ('experience', models.TextField(blank=True, max_length=1000, null=True)),
                ('prefer_sex', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('no preference', 'no preference')], max_length=200)),
                ('geographical', models.CharField(choices=[('EPA/MV', 'EPA/MV'), ('MP/RC', 'MP/RC'), ('SM', 'SM'), ('No preference', 'No preference')], max_length=200)),
                ('commit', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=False)),
                ('seminar', models.BooleanField(default=False)),
                ('signature', models.TextField(blank=True, max_length=1000, null=True)),
                ('grant', models.CharField(choices=[('Yes, I will find out and let you know.', 'Yes, I will find out and let you know.'), ('No, my corporation does not have this program.', 'No, my corporation does not have this program.'), ('No, I am currently not working at a corporation.', 'No, I am currently not working at a corporation.')], max_length=200)),
                ('check_bridge', models.BooleanField(default=False)),
                ('cont_student_bridge', models.TextField(blank=True, max_length=1000, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='mentors', to='mprofiles.Student')),
                ('reason', models.ManyToManyField(blank=True, related_name='mentorreasons', to='mprofiles.Mentorreason')),
                ('support', models.ManyToManyField(blank=True, related_name='supports', to='mprofiles.Support')),
            ],
        ),
    ]
