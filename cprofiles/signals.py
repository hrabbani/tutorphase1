from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Task, Tasksubject



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


@receiver(post_save, sender=Connection)
def post_save_create_task(sender, instance, created, **kwargs):
    if created:
        t = Task.objects.create(connection=instance, student=instance.student)
        for x in Tasksubject.objects.all():
            t.tasksubject.add(x)


# @receiver(post_save, sender=Task)
# def post_save_add_to_friends(sender, instance, created, **kwargs):
#     if not created:
#         connection_ = instance.connection
#         if instance.progress == 'off track':
#             connection_.flag = True
#             connection_.save()
#         if instance.progress == 'on track':
#             connection_.flag = False
#             connection_.save()


