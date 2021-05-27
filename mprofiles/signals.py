from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Session
import datetime
from django.core.mail import send_mail




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




@receiver(post_save, sender=Session)
def post_save_flag_session(sender, instance, created, **kwargs):

    list_a = list((instance.get_supports().values('name')))
    list_a = list(map(lambda x: x['name'], list_a))

    list_b = ['Engaging with mentees during session', 'Tech issues', 'Scheduling and communication issues', 'Other (please specify)']

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





def post_save_disconnect_connection(sender, instance, created, **kwargs):
    connection_ = instance.connection
    
    if instance.cont == 'no':
        connection_.status = 'disconnected'
        student = connection_.student
        mentor = connection_.mentor

        email_list = []
        email_list.append(student.email)
        email_list.append(mentor.email)
        email_list.append(student.academic_advisor_email)

        program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)

        content = "Connection is disconnected between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name
       
        send_mail('Connection Disconnected',
        content,
        'Mentor Program',
        email_list,
        fail_silently=False
        )      

        connection_.save()

        
post_save.connect(post_save_disconnect_connection, sender=Session, dispatch_uid="my_unique_identifier")





