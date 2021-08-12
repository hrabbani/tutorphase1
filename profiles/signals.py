from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Academicadvisor, Profile, Connection, Session, Subjectcalculation, Question
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import m2m_changed







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
    
    if not created:
        if instance.disconnect == 'no':
            connection_.status = 'disconnected'
            student = connection_.student
            tutor = connection_.tutor

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.academic_advisor_email)

            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("tutor/disconnection-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Peninsula Bridge: Tutoring Disconnection",
                text_context,
                'Tutoring Program',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection_.save()



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
        link = "http://127.0.0.1:8000/tutoring/" + session_generated_pk + "/session/"

        if instance.urgent_check == True:

            html_content = render_to_string("tutor/session-urgent-check-email.html", {'tutor_first_name': tutor_first_name, 'tutor_last_name': tutor_last_name,
             'date': date, 'tutor_email': tutor_email, 'question': question, 'link': link})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "[URGENT] Support Needed - Tutoring",
                text_context,
                'Tutoring Program',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

        else:
            pass