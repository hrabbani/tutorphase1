from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Connection, Session



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





@receiver(post_save, sender=Session)
def post_save_disconnect_connection(sender, instance, created, **kwargs):
    connection_ = instance.connection

    if instance.disconnect == 'yes':
        connection_.status = 'disconnected'
        connection_.save()



@receiver(post_save, sender=Session)
def post_save_flag_session(sender, instance, created, **kwargs):

    list_a = list((instance.get_supports().values('name')))
    list_a = list(map(lambda x: x['name'], list_a))

    list_b = ['Engaging with tutees during session', 'Tech issues', 'Scheduling and communication issues', 'My student didn’t show up']

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
