from django.db import models
from django.forms.models import ModelChoiceField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q




GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
)

GRADE_CHOICES = (
    ('5', '5'),
    ('8', '8'),
)

LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
)


        
class Student(models.Model):
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    grade = models.CharField(max_length=200, choices=GRADE_CHOICES)
    school = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    parent1_first_name = models.CharField(max_length=200, blank=True)
    parent1_last_name = models.CharField(max_length=200, blank=True)
    parent1_phone = models.CharField(max_length=200, blank=True)
    parent1_email = models.EmailField(max_length=200, blank=True)
    parent2_first_name = models.CharField(max_length=200, blank=True)
    parent2_last_name = models.CharField(max_length=200, blank=True)
    parent2_phone = models.CharField(max_length=200, blank=True)
    parent2_email = models.EmailField(max_length=200, blank=True)
    academic_advisor = models.CharField(max_length=200, blank=True)
    academic_advisor_email = models.EmailField(max_length=200, blank=True)
    parent_language = models.CharField(max_length=200, choices=LANGUAGE_CHOICES)
    activity = models.TextField(null=True, blank=True, max_length=1000)
    reason = models.TextField(null=True, blank=True, max_length=1000)
    prompt = models.TextField(null=True, blank=True, max_length=1000)
    hobby = models.TextField(null=True, blank=True, max_length=1000)
    parent_response = models.TextField(null=True, blank=True, max_length=1000)
    interview_language = models.CharField(max_length=200, choices=LANGUAGE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)


    
    def __str__(self):
        return f"{self.first_name}"

    def get_absolute_url(self):
        return reverse("cprofiles:student-profiles-detail", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.mentors.all()

    def get_friends_no(self):
        return self.mentors.all().count()


    def get_student_connections(self):
        return self.student.filter()


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name


    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Student.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Student.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)



MENTOR_GRADE_CHOICES = (
    ('5', '5'),
    ('8', '8'),
    ('no preference', 'no preference'),
)

class Mentor(models.Model):
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    prefer_grade = models.CharField(max_length=200, choices=MENTOR_GRADE_CHOICES)
    prefer_gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    prefer_location = models.CharField(max_length=200, blank=True)
    mentor_last_year = models.BooleanField(default=False)
    language = models.TextField(null=True, blank=True, max_length=1000)
    experience = models.TextField(null=True, blank=True, max_length=1000)
    familiar = models.TextField(null=True, blank=True, max_length=1000)
    friends = models.ManyToManyField(Student, blank=True, related_name='mentors')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)

    
    def __str__(self):
        return f"{self.first_name}"

    def get_absolute_url(self):
        return reverse("cprofiles:mentor-profiles-detail", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_mentor_connections(self):
        return self.mentor.filter()


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name


    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Mentor.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Mentor.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)




STATUS_CHOICES = (
    ('inactive', 'inactive'),
    ('connected', 'connected'),
    ('disconnected', 'disconnected'),
    ('off track', 'off track'),
)


PROGRESS_CHOICES = (
    ('on track', 'on track'),
    ('off track', 'off track'),
)



class Connection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    progress = models.CharField(max_length=200, blank=True, null=True, choices=PROGRESS_CHOICES)

    def __str__(self):
        return f"{self.student}-{self.mentor}-{self.status}"

    def get_absolute_url(self):
        return reverse("cprofiles:connection-profile-detail", kwargs={"pk": self.pk})

    def get_sessions(self):
        return self.session_set.filter(submit_status=True)[:1]

    def get_task(self):
        return self.task_set.all()

    def get_task(self):
        return self.task_set.get()

    def get_all_sessions(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')

    def get_all_sessions_four(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')[:4]


CONT_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
)


class Support(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name



class Topic(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name



class Session(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    meet = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    topic = models.ManyToManyField(Topic, blank=True, related_name='topics')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(null=True, blank=True, max_length=1000)
    change = models.TextField(null=True, blank=True, max_length=1000)
    support = models.ManyToManyField(Support, blank=True, related_name='supports')
    rate = models.IntegerField(null=True, blank=True)
    question = models.TextField(null=True, blank=True, max_length=1000)
    cont = models.CharField(null=True, blank=True, max_length=200, choices=CONT_STATUS_CHOICES)
    submit_status = models.BooleanField(default=False)
    step = models.CharField(max_length=200, blank=True)
    flag = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.connection.student.first_name}-{self.connection.mentor.first_name}"

    def get_topics(self):
        return self.topic.all()

    # def get_subjects_no(self):
    #     return self.subjects.all().count()

    def get_supports(self):
        return self.support.all()

    def get_absolute_url(self):
        return reverse("cprofiles:session-detail", kwargs={"pk": self.pk})

    def get_copytask(self):
        return self.copytask_set.get()


TASK_STATUS_CHOICES = (
    ('completed', 'completed'),
    ('not completed', 'not completed'),
)



class Tasksubject(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    duedate = models.DateField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True)
    tasksubject = models.ManyToManyField(Tasksubject, blank=True, related_name='tasksubject')
    task1status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task2status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task3status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task4status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task5status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task6status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task7status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task8status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task9status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task10status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    progress = models.CharField(max_length=200, blank=True, null=True, choices=PROGRESS_CHOICES)

    def __str__(self):
        return f"{self.id}"



class Copytask(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True)
    tasksubject = models.ManyToManyField(Tasksubject, blank=True)
    task1status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task2status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task3status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task4status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task5status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task6status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task7status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task8status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task9status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)
    task10status = models.CharField(max_length=200, blank=True, null=True, choices=TASK_STATUS_CHOICES)

    def __str__(self):
        return f"{self.id}"



