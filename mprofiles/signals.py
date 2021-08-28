from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Session, Academicadvisor, Student, Mentor, Question
import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags




@receiver(post_save, sender=Connection)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    student_ = instance.student
    mentor_ = instance.mentor
    if instance.status == 'connected':
        mentor_.friends.add(student_)
        mentor_.save()
    if instance.status == 'disconnected':
        mentor_.friends.remove(student_)
        mentor_.save()




# @receiver(post_save, sender=Session)
# def post_save_flag_session(sender, instance, created, **kwargs):

#     list_a = list((instance.get_supports().values('name')))
#     list_a = list(map(lambda x: x['name'], list_a))

#     list_b = ['Engaging with mentees during session', 'Scheduling and communication issues', 'Other (please specify)']

#     def common_member(a, b):
#         a_set = set(a)
#         b_set = set(b)
#         if (a_set & b_set):
#             return True 
#         else:
#             return False
          
#     if common_member(list_a, list_b) is True:
#         Session.objects.filter(pk=instance.id).update(flag=True)
#     else:
#         pass





# def post_save_disconnect_connection(sender, instance, created, **kwargs):
#     connection_ = instance.connection
    
#     if instance.cont == 'no':
#         connection_.status = 'disconnected'
#         student = connection_.student
#         mentor = connection_.mentor

#         email_list = []
#         email_list.append(student.email)
#         email_list.append(mentor.email)
#         email_list.append(student.academic_advisor_email)

#         program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
#         email_list.extend(program_manager_email_list)

#         content = "Connection is disconnected between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name
       
#         send_mail('Connection Disconnected',
#         content,
#         'Mentor Program',
#         email_list,
#         fail_silently=False
#         )      

#         connection_.save()

        
# post_save.connect(post_save_disconnect_connection, sender=Session, dispatch_uid="my_unique_identifier")



@receiver(post_save, sender=Student)
def post_save_student_form_academic_advisor_email_registration(sender, instance, created, **kwargs):

    if created:
        if Academicadvisor.objects.filter(name=instance.academic_advisor).exists():
            email = Academicadvisor.objects.get(name=instance.academic_advisor).email
            instance.academic_advisor_email = email
            instance.save()
        else:
            pass




@receiver(post_save, sender=Mentor)
def post_save_mentor_form_background_check(sender, instance, created, **kwargs):

    if created:
        if instance.check == 'no':
            email_list = []
            email_list.append(instance.email)

            html_content = render_to_string("mentor/background-check-email.html", {'mentor': instance })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "PB Mentoring Program Background Check",
                text_context,
                'Mentor Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()


@receiver(post_save, sender=Session)
def post_save_flag_session(sender, instance, created, **kwargs):

    if not created:

        session_generated_pk = str(instance.pk)

        email_list = []
        program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)

        form_link = "http://127.0.0.1:8000/mentoring/" + session_generated_pk + "/session/"

        if instance.urgent_check == True:
            html_content = render_to_string("mentor/session-urgent-support-email.html", {'session': instance, 'form_link': form_link})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "[URGENT] Feedback Form Submitted",
                text_context,
                'Mentor Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

        else:
            html_content = render_to_string("mentor/feedback-session-email.html", {'session': instance, 'form_link': form_link})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Feedback Form Submitted",
                text_context,
                'Mentor Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()


@receiver(post_save, sender=Mentor)
def post_save_mentor_form_question_registration(sender, instance, created, **kwargs):

    if created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance, question=instance.question, status="UNANSWERED", source="Sign-Up")
        else:
            pass


@receiver(post_save, sender=Session)
def post_save_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance.connection.mentor, question=instance.question, status="UNANSWERED", source="Feedback Form")
        else:
            pass




# @receiver(post_save, sender=Session)
# def post_save_session_support_registration(sender, instance, created, **kwargs):

#     if not created:
#         if instance.support:
#             Question.objects.get_or_create(mentor=instance.connection.mentor, question=instance.support, status="UNANSWERED", source="Feedback Form")
#         else:
#             pass



@receiver(post_save, sender=Session)
def post_save_session_flag_urgent_check(sender, instance, created, **kwargs):

    if not created:
        
        if instance.urgent_check == True:
            Session.objects.filter(pk=instance.id).update(flag=True)
        
        else:
            pass