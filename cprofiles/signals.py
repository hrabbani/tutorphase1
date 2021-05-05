from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Session, Task, Tasksubject, Copytask
import datetime



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


@receiver(post_save, sender=Task)
def post_save_update_session(sender, instance, created, **kwargs):
    if not created:

        connection = Connection.objects.get(task__pk=instance.pk)

        try:
            session = Session.objects.filter(connection=connection).latest('updated')
        except:
            pass

        try:
            if instance.task10status == 'completed':
                name = instance.tasksubject.all()[9].name
                session.step = name
                session.save()
            
            elif instance.task9status == 'completed':
                name = instance.tasksubject.all()[8].name
                session.step = name
                session.save()

                    
            elif instance.task8status == 'completed':
                name = instance.tasksubject.all()[7].name
                session.step = name
                session.save()

                    
            elif instance.task7status == 'completed':
                name = instance.tasksubject.all()[6].name
                session.step = name
                session.save()
            
                    
            elif instance.task6status == 'completed':
                name = instance.tasksubject.all()[5].name
                session.step = name
                session.save()

                    
            elif instance.task5status == 'completed':
                name = instance.tasksubject.all()[4].name
                session.step = name
                session.save()

                    
            elif instance.task4status == 'completed':
                name = instance.tasksubject.all()[3].name
                session.step = name
                session.save()

                    
            elif instance.task3status == 'completed':
                name = instance.tasksubject.all()[2].name
                session.step = name
                session.save()

                    
            elif instance.task2status == 'completed':
                name = instance.tasksubject.all()[1].name
                session.step = name
                session.save()

            elif instance.task1status == 'completed':
                name = instance.tasksubject.all()[0].name
                session.step = name
                session.save()

        except:
            pass





@receiver(post_save, sender=Task)
def post_save_update_connection(sender, instance, created, **kwargs):
    if not created:

        today_date = datetime.date.today()

        instance.connection.flag = False
        instance.connection.save()
        instance.connection.progress = 'on track'
        instance.connection.save()
        if instance.task1status == None:
            instance.connection.progress = None
            instance.connection.save()
        if instance.task1status == 'not completed':
            if instance.tasksubject.all()[0].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task2status == 'not completed':
            if instance.tasksubject.all()[1].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task3status == 'not completed':
            if instance.tasksubject.all()[2].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task4status == 'not completed':
            if instance.tasksubject.all()[3].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task5status == 'not completed':
            if instance.tasksubject.all()[4].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task6status == 'not completed':
            if instance.tasksubject.all()[5].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task7status == 'not completed':
            if instance.tasksubject.all()[6].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task8status == 'not completed':
            if instance.tasksubject.all()[7].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task9status == 'not completed':
            if instance.tasksubject.all()[8].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()
        if instance.task10status == 'not completed':
            if instance.tasksubject.all()[9].duedate < today_date:
                instance.connection.flag = True
                instance.connection.progress = 'off track'
                instance.connection.save()





@receiver(post_save, sender=Task)
def post_save_create_copy_task(sender, instance, created, **kwargs):
    if not created:

        connection = Connection.objects.get(task__pk=instance.pk)

        try:
            session = Session.objects.filter(connection=connection).latest('updated')
        except:
            pass

        try:
            copy_task = Copytask.objects.create(session=session, task1status=instance.task1status, task2status=instance.task2status, task3status=instance.task3status, task4status=instance.task4status, task5status=instance.task5status, task6status=instance.task6status, task7status=instance.task7status, task8status=instance.task8status, task9status=instance.task9status, task10status=instance.task10status)
        except:
            pass
 






