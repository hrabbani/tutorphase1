from django.db import connection
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Connection, Session, Task, Tasksubject, Copytask, Student, Mentor, Question, Topiccalculation, Parentsession
import datetime
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
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
    if instance.status == 'off track':

        email_list = []
        program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)

        content = "Choice Program: Off-Track Progress -" + mentor_.first_name + " " + mentor_.last_name + " and " + student_.first_name + " " + student_.last_name

        pk = instance.pk

        link = "http://127.0.0.1:8000/choice/" + str(pk) + "/connection-detail"

        html_content = render_to_string("choice/connection-offtrack-email.html", {'connection': instance, 'form_link': link})
        text_context = strip_tags(html_content)
        email = EmailMultiAlternatives(
            content,
            text_context,
            'Choice Program - Peninsula Bridge',
            email_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()


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
                Session.objects.filter(id=session.id).update(step=name)
                
            
            elif instance.task9status == 'completed':
                name = instance.tasksubject.all()[8].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task8status == 'completed':
                name = instance.tasksubject.all()[7].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task7status == 'completed':
                name = instance.tasksubject.all()[6].name
                Session.objects.filter(id=session.id).update(step=name)

            
                    
            elif instance.task6status == 'completed':
                name = instance.tasksubject.all()[5].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task5status == 'completed':
                name = instance.tasksubject.all()[4].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task4status == 'completed':
                name = instance.tasksubject.all()[3].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task3status == 'completed':
                name = instance.tasksubject.all()[2].name
                Session.objects.filter(id=session.id).update(step=name)


                    
            elif instance.task2status == 'completed':
                name = instance.tasksubject.all()[1].name
                Session.objects.filter(id=session.id).update(step=name)


            elif instance.task1status == 'completed':
                name = instance.tasksubject.all()[0].name
                Session.objects.filter(id=session.id).update(step=name)


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
            Question.objects.get_or_create(student=instance, role='Student/Parent', question=instance.question, status="UNANSWERED", source='Student Sign-Up')
        else:
            pass



@receiver(post_save, sender=Mentor)
def post_save_mentor_form_question_registration(sender, instance, created, **kwargs):

    if created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance, role='Mentor', question=instance.question, status="UNANSWERED", source='Mentor Sign-Up')
        else:
            pass



@receiver(post_save, sender=Session)
def post_save_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(mentor=instance.connection.mentor, role='Mentor', question=instance.question, status="UNANSWERED", source='Mentor Feedback')
        else:
            pass


@receiver(post_save, sender=Parentsession)
def post_save_parent_session_question_registration(sender, instance, created, **kwargs):

    if not created:
        if instance.question:
            Question.objects.get_or_create(student=instance.connection.student, role='Student/Parent', question=instance.question, status="UNANSWERED", source='Student/Parent Feedback')
        else:
            pass


def post_save_topic_registration(sender, instance, **kwargs):

    if instance.get_topics():
        for x in instance.get_topics():
            Topiccalculation.objects.create(name=x)
    else:
        pass

m2m_changed.connect(post_save_topic_registration, sender=Session.topic.through)




@receiver(post_save, sender=Parentsession)
def post_save_urgent_check_session(sender, instance, created, **kwargs):

    if not created:

        session_generated_pk = str(instance.pk)

        email_list = []
        program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)


        student_first_name = instance.connection.student.first_name
        student_last_name = instance.connection.student.last_name
        student_email = instance.connection.student.email
        question = instance.question
        link = "http://127.0.0.1:8000/choice/" + session_generated_pk + "/parent-session/"

        if instance.urgent_check == True:

            html_content = render_to_string("choice/parent-session-urgent-check-email.html", {'student_first_name': student_first_name, 'student_last_name': student_last_name, 'student_email': student_email, 'question': question, 'link': link})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "[URGENT] Support Needed - Student",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

        else:
            pass



@receiver(post_save, sender=Session)
def post_save_urgent_check_mentor_session(sender, instance, created, **kwargs):

    if not created:

        session_generated_pk = str(instance.pk)

        email_list = []
        program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
        email_list.extend(program_manager_email_list)


        mentor_first_name = instance.connection.mentor.first_name
        mentor_last_name = instance.connection.mentor.last_name
        mentor_email = instance.connection.mentor.email
        elaborate = instance.elaborate
        link = "http://127.0.0.1:8000/choice/" + session_generated_pk + "/session/"

        if instance.urgent_check == True:

            html_content = render_to_string("choice/session-urgent-check-email.html", {'mentor_first_name': mentor_first_name, 'mentor_last_name': mentor_last_name, 'mentor_email': mentor_email, 'elaborate': elaborate, 'link': link})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "[URGENT] Support Needed - Mentor",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

        else:
            pass







@receiver(post_save, sender=Session)
def post_save_session_update_submit_status(sender, instance, created, **kwargs):

    if not created:
        Session.objects.filter(pk=instance.id).update(submit_status=True)
    else:
        pass



