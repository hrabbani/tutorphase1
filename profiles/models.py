from django.db import models
from django.forms.models import ModelChoiceField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


class Subject(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name




ROLE_CHOICES_PROFILE = (
    ('tutor', 'tutor'),
    ('student', 'student')
)
        
class Profile(models.Model):
    role = models.CharField(max_length=200, choices=ROLE_CHOICES_PROFILE, null=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='subjects')
    school = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField("self", blank=True, related_name='testfriends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)


    
    def __str__(self):
        return f"{self.first_name}-{self.role}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_subjects(self):
        return self.subjects.all()
 

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
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)




STATUS_CHOICES = (
    ('inactive', 'inactive'),
    ('connected', 'connected'),
    ('disconnected', 'disconnected')
)


class Connection(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='student')
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tutor')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student}-{self.tutor}-{self.status}"

    def get_absolute_url(self):
        return reverse("profiles:connection-detail-view", kwargs={"pk": self.pk})

    def get_sessions(self):
        return self.session_set.filter(submit_status=True)[:1]


CONT_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
)


class Support(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    meet = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='sessionsubjects')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(null=True, blank=True, max_length=1000)
    change = models.TextField(null=True, blank=True, max_length=1000)
    support = models.ManyToManyField(Support, blank=True, related_name='supports')
    othersupport = models.CharField(null=True, blank=True, max_length=200)
    question = models.TextField(null=True, blank=True, max_length=1000)
    cont = models.CharField(null=True, blank=True, max_length=200, choices=CONT_STATUS_CHOICES)
    submit_status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.connection.student.first_name}-{self.connection.tutor.first_name}"

    def get_subjects(self):
        return self.subjects.all()

    def get_subjects_no(self):
        return self.subjects.all().count()

    def get_supports(self):
        return self.support.all()

    def get_absolute_url(self):
        return reverse("profiles:session-detail-view", kwargs={"pk": self.pk})
