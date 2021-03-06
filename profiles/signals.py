from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Academicadvisor, Profile, Connection, Session, Subjectcalculation, Question
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import m2m_changed
import environ
import os

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

EMAIL_USERNAME_HIGH_SCHOOL=env('email_username_high_school')
EMAIL_PASSWORD_HIGH_SCHOOL=env('email_password_high_school')

connection = get_connection(host='smtp.gmail.com', 
                                port=587, 
                                username=EMAIL_USERNAME_HIGH_SCHOOL, 
                                password=EMAIL_PASSWORD_HIGH_SCHOOL, 
                                use_tls=True)




@receiver(post_save, sender=Connection)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    student_ = instance.student
    tutor_ = instance.tutor
    if instance.status == 'connected':
        student_.friends.add(tutor_)
        tutor_.friends.add(student_)
        student_.save()
        tutor_.save()
    if instance.status == 'disconnected':
        student_.friends.remove(tutor_)
        tutor_.friends.remove(student_)
        student_.save()
        tutor_.save()



@receiver(post_save, sender=Session, dispatch_uid="my_unique_identifier")
def post_save_disconnect_connection(sender, instance, created, **kwargs):
    connection_ = instance.connection

    global connection
    
    if not created:
        if instance.disconnect == 'no':
            student = connection_.student
            tutor = connection_.tutor

            email_list = []
            # email_list.append(student.email)
            # email_list.append(tutor.email)
            # email_list.append(student.parent1_email)
            email_list.append(student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            content = "Tutoring Disconnection Requested - " + tutor.first_name  + " and " + student.first_name

            connection_pk = str(connection_.pk)
            connection_link = "https://www.admin.peninsulabridge.org/tutoring/" + connection_pk + "/connection-detail/"


            html_content = render_to_string("tutor/feedback-disconnection-email.html", {'student': student, 'tutor': tutor, 'connection_link': connection_link, 'session': instance  })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                content,
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()



def post_save_flag_session(sender, instance, **kwargs):

    list_a = list((instance.get_supports().values('name')))
    list_a = list(map(lambda x: x['name'], list_a))

    list_b = ['Engaging with tutees during session', 'Tech issues (e.g. wifi connection, camera issue)', 'Scheduling and communication issues', 'My student is unmotivated', 'Creating curriculum / session material']

    def common_member(a, b):
        a_set = set(a)
        b_set = set(b)
        if (a_set & b_set):
            return True 
        else:
            return False
          
    if common_member(list_a, list_b) is True:
        Session.objects.filter(pk=instance.id).update(flag=True)
    else:
        pass

m2m_changed.connect(post_save_flag_session, sender=Session.support.through)



def post_save_subject_registration(sender, instance, **kwargs):

    if instance.get_subjects():
        for x in instance.get_subjects():
            Subjectcalculation.objects.create(name=x)
    else:
        pass

m2m_changed.connect(post_save_subject_registration, sender=Session.subjects.through)



@receiver(post_save, sender=Session)
def post_save_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(tutor=instance.connection.tutor, question=instance.question, status="UNANSWERED", source="Feedback Form")
        else:
            pass


@receiver(post_save, sender=Profile)
def post_save_tutor_form_question_registration(sender, instance, created, **kwargs):

    if created:
        if instance.question:
            Question.objects.get_or_create(tutor=instance, question=instance.question, status="UNANSWERED", source="Sign-Up")
        else:
            pass



@receiver(post_save, sender=Profile)
def post_save_tutor_form_academic_advisor_email_registration(sender, instance, created, **kwargs):

    if created:
        if Academicadvisor.objects.filter(name=instance.academic_advisor).exists():
            email = Academicadvisor.objects.get(name=instance.academic_advisor).email
            instance.academic_advisor_email = email
            instance.save()
        else:
            pass



@receiver(post_save, sender=Session)
def post_save_urgent_check_session(sender, instance, created, **kwargs):

    global connection

    if not created:

        session_generated_pk = str(instance.pk)

        email_list = []
        program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)


        tutor_first_name = instance.connection.tutor.first_name
        tutor_last_name = instance.connection.tutor.last_name
        date = instance.updated
        tutor_email = instance.connection.tutor.email
        question = instance.question
        link = "https://www.admin.peninsulabridge.org/tutoring/" + session_generated_pk + "/session/"

        if instance.urgent_check == True:

            html_content = render_to_string("tutor/session-urgent-check-email.html", {'tutor_first_name': tutor_first_name, 'tutor_last_name': tutor_last_name,
             'date': date, 'tutor_email': tutor_email, 'question': question, 'link': link})
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "[URGENT] Support Needed - Tutoring",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()
            connection.close()

        else:
            pass


@receiver(post_save, sender=Profile)
def post_save_tutor_form_background_check(sender, instance, created, **kwargs):

    global connection

    if created:
        if instance.check == 'yes':
            email_list = []
            email_list.append(instance.email)

            html_content = render_to_string("tutor/background-check-email.html", {'tutor': instance })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "PB Tutoring Program Background Check",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()