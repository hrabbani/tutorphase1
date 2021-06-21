from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Session, Task, Tasksubject, Copytask, Student, Mentor, Question, Topiccalculation, Parentsession
import datetime
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed





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
    if instance.status == 'off track':
        email_list = []
        email_list.append(student_.academic_advisor_email)
        email_list.append(mentor_.email)

        program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)

        content = "Connection is 'Off Track' between Student " + student_.first_name + " " + student_.last_name + " " + "Mentor" + " " + mentor_.first_name + " " + mentor_.last_name
       
        send_mail('Connection Off Track',
        content,
        'Choice Program',
        email_list,
        fail_silently=False
        )  



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
            try:
                if instance.tasksubject.all()[0].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task2status == 'not completed':
            try:
                if instance.tasksubject.all()[1].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task3status == 'not completed':
            try:
                if instance.tasksubject.all()[2].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task4status == 'not completed':
            try:
                if instance.tasksubject.all()[3].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task5status == 'not completed':
            try:
                if instance.tasksubject.all()[4].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task6status == 'not completed':
            try:
                if instance.tasksubject.all()[5].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task7status == 'not completed':
            try:
                if instance.tasksubject.all()[6].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task8status == 'not completed':
            try:
                if instance.tasksubject.all()[7].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task9status == 'not completed':
            try:
                if instance.tasksubject.all()[8].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass
        if instance.task10status == 'not completed':
            try:
                if instance.tasksubject.all()[9].duedate < today_date:
                    instance.connection.flag = True
                    instance.connection.progress = 'off track'
                    instance.connection.status = 'off track'
                    instance.connection.save()
            except:
                pass


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
 



@receiver(post_save, sender=Student)
def post_save_student_form_question_registration(sender, instance, created, **kwargs):

    if created:
        if instance.question:
            Question.objects.get_or_create(student=instance, role='Student/Parent', question=instance.question, status="UNANSWERED")
        else:
            pass



@receiver(post_save, sender=Mentor)
def post_save_mentor_form_question_registration(sender, instance, created, **kwargs):

    if created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance, role='Mentor', question=instance.question, status="UNANSWERED")
        else:
            pass



@receiver(post_save, sender=Session)
def post_save_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance.connection.mentor, role='Mentor', question=instance.question, status="UNANSWERED")
        else:
            pass


@receiver(post_save, sender=Parentsession)
def post_save_parent_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(student=instance.connection.student, role='Student/Parent', question=instance.question, status="UNANSWERED")
        else:
            pass


def post_save_topic_registration(sender, instance, **kwargs):

    if instance.get_topics():
        for x in instance.get_topics():
            Topiccalculation.objects.create(name=x)
    else:
        pass

m2m_changed.connect(post_save_topic_registration, sender=Session.topic.through)

