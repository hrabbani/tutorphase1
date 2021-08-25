from django.db import models
from django.forms.models import ModelChoiceField
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver




YES_NO = (
    ('yes', 'yes'),
    ('no', 'no'),
)

class Academicadvisor(models.Model):

    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)

    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('no preference', 'no preference')
)


QUESTION_CHOICES = (
    ('What was the first job you wanted as a kid?', 'What was the first job you wanted as a kid?'),
    ('If you were one of the seven dwarves in Snow White, which one would you be?', 'If you were one of the seven dwarves in Snow White, which one would you be?'),
    ('What is your guilty pleasure?', 'What is your guilty pleasure?'),
    ('What song do you sing in the shower?', 'What song do you sing in the shower?'),
    ('What is your biggest (non-serious) fear?', 'What is your biggest (non-serious) fear?'),
    ('What is your favorite binge-watching TV series?', 'What is your favorite binge-watching TV series?'),
    ('What would your last meal on Earth be?', 'What would your last meal on Earth be?'),
    ('Who is your favorite person in history?', 'Who is your favorite person in history?'),
    ('A trip you most want to take but haven’t yet?', 'A trip you most want to take but haven’t yet?'),
)


GEOGRAPHICAL_CHOICES = (
    ('East Palo Alto/Mountain View', 'East Palo Alto/Mountain View'),
    ('Menlo Park/Redwood City', 'Menlo Park/Redwood City'),
    ('San Mateo', 'San Mateo'),
    ('No preference', 'No preference')

)



        
class Student(models.Model):
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    grade = models.CharField(max_length=200, blank=True)
    school = models.CharField(max_length=200, blank=True)
    academic_advisor = models.ForeignKey(Academicadvisor, null=True, blank=True, on_delete=models.CASCADE, related_name='academic_advisor')
    academic_advisor_email = models.EmailField(max_length=200, blank=True)
    reason = models.TextField(null=True, blank=True, max_length=1000)
    know = models.TextField(null=True, blank=True, max_length=1000)
    question1 = models.CharField(max_length=200, choices=QUESTION_CHOICES)
    answer1 = models.TextField(null=True, blank=True, max_length=1000)
    question2 = models.CharField(max_length=200, choices=QUESTION_CHOICES)
    answer2 = models.TextField(null=True, blank=True, max_length=1000)
    prefer_sex = models.CharField(max_length=200, choices=GENDER_CHOICES)
    geographical = models.CharField(max_length=200, choices=GEOGRAPHICAL_CHOICES)
    commit = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    available = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    seminar = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    understand = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    signature = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True, max_length=1000)

    
    def __str__(self):
        return f"{self.first_name}"

    def get_absolute_url(self):
        return reverse("mprofiles:student-profiles-detail", kwargs={"slug": self.slug})

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




EMPLOYMENT_CHOICES = (
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Unemployed', 'Unemployed'),
    ('Retired', 'Retired')
)

GRANT_CHOICES = (
    ('Yes, I will find out and let you know.', 'Yes, I will find out and let you know.'),
    ('No, my corporation does not have this program.', 'No, my corporation does not have this program.'),
    ('No, I am currently not working at a corporation.', 'No, I am currently not working at a corporation.'),
)




class Support(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

SPANISH_CHOICES = (
    ('Not at all', 'Not at all'),
    ('Low (can make basic conversation)', 'Low (can make basic conversation)'),
    ('Medium (somewhat fluent)', 'Medium (somewhat fluent)'),
    ('High (proficient enough to have a lengthy and detailed conversation)', 'High (proficient enough to have a lengthy and detailed conversation)'),
)


PARTNER_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
    ('unsure', 'unsure')
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

class Mentor(models.Model):
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    spanish = models.CharField(null=True, blank=True, max_length=200, choices=SPANISH_CHOICES)
    language = models.TextField(null=True, blank=True, max_length=1000)
    emergency_contact = models.TextField(null=True, blank=True, max_length=1000)
    employment_status = models.CharField(max_length=200, choices=EMPLOYMENT_CHOICES)
    employer_info = models.TextField(null=True, blank=True, max_length=1000)
    partner = models.CharField(null=True, blank=True, max_length=200, choices=PARTNER_CHOICES)
    hear = models.TextField(null=True, blank=True, max_length=1000)
    experience = models.TextField(null=True, blank=True, max_length=1000)
    reason = models.TextField(null=True, blank=True, max_length=1000)
    know = models.TextField(null=True, blank=True, max_length=1000)
    question1 = models.CharField(null=True, blank=True, max_length=200, choices=QUESTION_CHOICES)
    answer1 = models.TextField(null=True, blank=True, max_length=1000)
    question2 = models.CharField(null=True, blank=True, max_length=200, choices=QUESTION_CHOICES)
    answer2 = models.TextField(null=True, blank=True, max_length=1000)
    support = models.ManyToManyField(Support, blank=True, related_name='supports')
    prefer_sex = models.CharField(max_length=200, choices=GENDER_CHOICES)
    geographical = models.CharField(max_length=200, choices=GEOGRAPHICAL_CHOICES)
    commit = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    available = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    seminar = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    signature = models.TextField(null=True, blank=True, max_length=1000)
    grant = models.CharField(max_length=200, choices=GRANT_CHOICES)
    cont_student_bridge = models.TextField(null=True, blank=True, max_length=1000)
    check = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    question = models.TextField(null=True, blank=True, max_length=1000)
    friends = models.ManyToManyField(Student, blank=True, related_name='mentors')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    flag = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True, max_length=1000)
    ethnic = models.CharField(null=True, blank=True, max_length=200, choices=ETHNIC_CHOICES)




    def __str__(self):
        return f"{self.first_name}"

    def get_absolute_url(self):
        return reverse("mprofiles:mentor-profiles-detail", kwargs={"slug": self.slug})

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
)




class Connection(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    flag = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True, max_length=1000)


    def __str__(self):
        return f"{self.student}-{self.mentor}-{self.status}"

    def get_absolute_url(self):
        return reverse("mprofiles:connection-profile-detail", kwargs={"pk": self.pk})

    def get_sessions(self):
        return self.session_set.filter(submit_status=True)[:1]

    def get_all_sessions(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')

    def get_all_sessions_two(self):
        return self.session_set.filter(submit_status=True).order_by('-updated')[:2]



CONT_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
)


class Sessionsupport(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    meet = models.IntegerField(null=True, blank=True)
    dialogue = models.CharField(null=True, blank=True, max_length=200, choices=YES_NO)
    length = models.FloatField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True, max_length=1000)
    help = models.TextField(null=True, blank=True, max_length=1000)
    change = models.TextField(null=True, blank=True, max_length=1000)
    rate = models.IntegerField(null=True, blank=True)
    meaningful = models.IntegerField(null=True, blank=True)
    support = models.TextField(null=True, blank=True, max_length=1000)
    elaborate = models.TextField(null=True, blank=True, max_length=1000)
    urgent = models.TextField(null=True, blank=True, max_length=1000)
    question = models.TextField(null=True, blank=True, max_length=1000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    submit_status = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    urgent_check = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.connection.student.first_name}-{self.connection.mentor.first_name}"

    def get_absolute_url(self):
        return reverse("mprofiles:session-detail", kwargs={"pk": self.pk})


QUESTION_STATUS_CHOICES = (
    ('UNANSWERED', 'UNANSWERED'),
    ('ADDRESSED', 'ADDRESSED'),

)

class Question(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_question')
    question = models.TextField(null=True, blank=True, max_length=1000)
    action = models.BooleanField(default=False)
    status = models.CharField(null=True, blank=True, max_length=200, choices=QUESTION_STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.question