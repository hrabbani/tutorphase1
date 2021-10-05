from django.db import models
from django.forms.models import ModelChoiceField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone



class Academicadvisor(models.Model):

    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Interest(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Parentlanguage(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


ROLE_CHOICES_PROFILE = (
    ('tutor', 'tutor'),
    ('student', 'student')
)


LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
)

STUDENT_GRADE_CHOICES = (
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
)


GRADE_CHOICES = (
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('Not in grade school', 'Not in grade school'),
)


ETHNIC_CHOICES = (
    ('African American or Black', 'African American or Black'),
    ('American Indian or Alaskan Native', 'American Indian or Alaskan Native'),
    ('Asian American', 'Asian American'),
    ('Caucasian or White', 'Caucasian or White'),
    ('Hispanic or Latino', 'Hispanic or Latino'),
    ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'),
    ('I prefer not to say', 'I prefer not to say')
)


YES_NO = (
    ('yes', 'yes'),
    ('no', 'no'),
)

PROFILE_STATUS = (
    ('active', 'active'),
    ('deactivated', 'deactivated'),
)
        
class Profile(models.Model):
    role = models.CharField(max_length=200, choices=ROLE_CHOICES_PROFILE, null=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    student_grade = models.CharField(null=True, blank=True, max_length=200, choices=STUDENT_GRADE_CHOICES)
    grade = models.CharField(null=True, blank=True, max_length=200, choices=GRADE_CHOICES)
    academic_advisor = models.ForeignKey(Academicadvisor, null=True, blank=True, on_delete=models.CASCADE, related_name='academic_advisor')
    academic_advisor_email = models.EmailField(max_length=200, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='subjects')
    school = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField("self", blank=True, related_name='testfriends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)
    parent1_first_name = models.CharField(max_length=200, blank=True)
    parent1_last_name = models.CharField(max_length=200, blank=True)
    parent1_phone = models.CharField(max_length=200, blank=True)
    parent1_email = models.EmailField(max_length=200, blank=True)
    student_capacity = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    question = models.TextField(null=True, blank=True, max_length=1000)
    languages = models.ManyToManyField(Language, blank=True, related_name='subjects')
    comfortable_share_phone = models.BooleanField(default=False)
    permission_share_grade = models.BooleanField(default=False)
    optional_school_loop_profile_link = models.TextField(null=True, blank=True, max_length=500)
    optional_school_loop_username = models.TextField(null=True, blank=True, max_length=500)
    optional_school_loop_password = models.TextField(null=True, blank=True, max_length=500)
    parent_languages = models.CharField(null=True, blank=True, max_length=200, choices=LANGUAGE_CHOICES)
    age = models.IntegerField(null=True, blank=True)
    ethnic = models.CharField(null=True, blank=True, max_length=200, choices=ETHNIC_CHOICES)
    note = models.TextField(null=True, blank=True, max_length=1000)
    interest = models.ManyToManyField(Interest, blank=True, related_name='interest')
    check = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    status = models.CharField(null=True, blank=True, max_length=200, choices=PROFILE_STATUS, default='active')

    
    def __str__(self):
        return f"{self.first_name}-{self.role}"

    def get_absolute_url(self):
        return reverse("middleschool:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_subjects(self):
        return self.subjects.all()

    def get_languages(self):
        return self.languages.all()

    def get_tutor_connections(self):
        return self.tutor.filter()
 
    def get_student_connections(self):
        return self.student.filter()

    def get_interests(self):
        return self.interest.all()

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
    flag = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True, max_length=1000)



    def __str__(self):
        return f"{self.student}-{self.tutor}-{self.status}"

    def get_absolute_url(self):
        return reverse("middleschool:connection-detail-view", kwargs={"pk": self.pk})

    def get_sessions(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')[:1]

    def get_all_sessions(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')

    def get_all_sessions_three(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')[:3]

    def get_all_sessions_three_feedback_status(self):
        return self.session_set.filter().order_by('-created')[:3]

        

CONT_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
)


class Support(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):

    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    meet = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='sessionsubjects')
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    help = models.TextField(null=True, blank=True, max_length=1000)
    support = models.ManyToManyField(Support, blank=True, related_name='supports')
    othersupport = models.CharField(null=True, blank=True, max_length=200)
    rate = models.IntegerField(null=True, blank=True)
    productivity = models.IntegerField(null=True, blank=True)
    question = models.TextField(null=True, blank=True, max_length=1000)
    disconnect = models.CharField(null=True, blank=True, max_length=200, choices=CONT_STATUS_CHOICES)
    submit_status = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    reason_disconnect= models.TextField(null=True, blank=True, max_length=1000)
    urgent_check = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.connection.student.first_name}-{self.connection.tutor.first_name}"

    def get_subjects(self):
        return self.subjects.all()

    def get_subjects_no(self):
        return self.subjects.all().count()

    def get_supports(self):
        return self.support.all()
    
    def get_questions(self):
        return self.question

    def get_absolute_url(self):
        return reverse("middleschool:session-detail-view", kwargs={"pk": self.pk})



class Subjectcalculation(models.Model):

    name = models.CharField(max_length=200, blank=True)
    updated = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name




QUESTION_STATUS_CHOICES = (
    ('UNANSWERED', 'UNANSWERED'),
    ('ADDRESSED', 'ADDRESSED'),

)

class Question(models.Model):
    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tutor_question')
    question = models.TextField(null=True, blank=True, max_length=1000)
    action = models.BooleanField(default=False)
    status = models.CharField(null=True, blank=True, max_length=200, choices=QUESTION_STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.question