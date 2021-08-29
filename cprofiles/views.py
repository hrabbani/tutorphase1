from django.template.defaultfilters import length
from cprofiles.models import Student, Mentor, Connection, Task, Tasksubject, Session, Question, Topiccalculation, Parentsession
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mentor, Student
from .forms import TaskModelForm, SessionModelForm, MentorModelForm, StudentModelForm, ParentSessionModelForm, StudentNoteModelForm, ConnectionNoteModelForm
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
import json
from datetime import timedelta
from datetime import date
from django.db.models import Sum, Avg
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
import collections
from django.urls import reverse_lazy, reverse
import datetime
from itertools import chain
from core.decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
import csv
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags






@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class MentorProfileListView(ListView):
    model = Mentor
    template_name = 'choice/mentor-profile-list.html'

    def get_queryset(self):
        qs = Mentor.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipients = list(i for i in Mentor.objects.values_list('email', flat=True))
        recipients = ("; ".join(recipients))
        context["recipients"] = recipients
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class StudentProfileListView(ListView):
    model = Student
    template_name = 'choice/choice-student-profile-list.html'

    def get_queryset(self):
        qs = Student.objects.all()
        return qs


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class MentorDetailView(DetailView):
    model = Mentor
    template_name = 'choice/mentor-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        mentor = Mentor.objects.get(slug=slug)
        return mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        mentor = Mentor.objects.get(slug=slug)
        sessions = Session.objects.filter(submit_status=True).filter(connection__mentor=mentor)
        sessions_ = []
        for item in sessions:
            sessions_.append(item)
        context["sessions"] = sessions_
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class MentorUpdateView(UpdateView):
    form_class = MentorModelForm
    model = Mentor
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("cprofiles:mentor-profiles-detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class StudentUpdateView(UpdateView):
    form_class = StudentModelForm
    model = Student
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("cprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = 'choice/student-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        mentor = Student.objects.get(slug=slug)
        return mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        student = Student.objects.get(slug=slug)
        sessions = Session.objects.filter(submit_status=True).filter(connection__student=student)
        sessions_ = []
        for item in sessions:
            sessions_.append(item)
        context["sessions"] = sessions_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class MentorProfileDetailView(DetailView):
    model = Mentor
    template_name = 'choice/mentor-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        mentor = Mentor.objects.get(slug=slug)
        return mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        students_ = []
        for item in students:
            students_.append(item)
        context["students"] = students_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class StudentProfileDetailView(DetailView):
    model = Student
    template_name = 'choice/choice-student-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        student = Student.objects.get(slug=slug)
        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentors = Mentor.objects.all()
        mentors_ = []
        for item in mentors:
            mentors_.append(item)
        context["mentors"] = mentors_
        return context



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def mentor_connect(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        mentor_pk = request.POST.get('mentor_pk')
        student = Student.objects.get(pk=student_pk)
        mentor = Mentor.objects.get(pk=mentor_pk)

        exist_connection = Connection.objects.filter(student=student).filter(mentor=mentor)

        if exist_connection.exists():
            exist_connection = Connection.objects.get(Q(student=student), Q(mentor=mentor))
            exist_connection.status = 'connected'
            exist_connection.save()

            email_list = []
            email_list.append(student.email)
            email_list.append(student.parent1_email)

            html_content = render_to_string("choice/connection-email.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Mentor Connection for Choice Program",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            #Email to Mentor

            email_mentor = []
            email_mentor.append(mentor.email)

            html_content = render_to_string("choice/connection-email-to-mentor.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email_to_mentor = EmailMultiAlternatives(
                "Mentor Pairing - Choice Program 2021",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_mentor,
            )

            email_to_mentor.attach_alternative(html_content, "text/html")
            email_to_mentor.send()


        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(student.parent1_email)

            html_content = render_to_string("choice/connection-email.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Mentor Connection for Choice Program",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            #Email to Mentor

            email_mentor = []
            email_mentor.append(mentor.email)

            html_content = render_to_string("choice/connection-email-to-mentor.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email_to_mentor = EmailMultiAlternatives(
                "Mentor Pairing - Choice Program 2021",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_mentor,
            )

            email_to_mentor.attach_alternative(html_content, "text/html")
            email_to_mentor.send()
 
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cprofiles:mentor-profiles-list')




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def student_connect(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        mentor_pk = request.POST.get('mentor_pk')
        student = Student.objects.get(pk=student_pk)
        mentor = Mentor.objects.get(pk=mentor_pk)

        exist_connection = Connection.objects.filter(student=student).filter(mentor=mentor)

        if exist_connection.exists():
            exist_connection = Connection.objects.get(Q(student=student), Q(mentor=mentor))
            exist_connection.status = 'connected'
            exist_connection.save()

            email_list = []
            email_list.append(student.email)
            email_list.append(student.parent1_email)

            html_content = render_to_string("choice/connection-email.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Mentor Connection for Choice Program",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            #Email to Mentor

            email_mentor = []
            email_mentor.append(mentor.email)

            html_content = render_to_string("choice/connection-email-to-mentor.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email_to_mentor = EmailMultiAlternatives(
                "Mentor Pairing - Choice Program 2021",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_mentor,
            )

            email_to_mentor.attach_alternative(html_content, "text/html")
            email_to_mentor.send()
            
        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(student.parent1_email)

            html_content = render_to_string("choice/connection-email.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Mentor Connection for Choice Program",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            #Email to Mentor

            email_mentor = []
            email_mentor.append(mentor.email)

            html_content = render_to_string("choice/connection-email-to-mentor.html", {'student': student, 'mentor': mentor })
            text_context = strip_tags(html_content)
            email_to_mentor = EmailMultiAlternatives(
                "Mentor Pairing - Choice Program 2021",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_mentor,
            )

            email_to_mentor.attach_alternative(html_content, "text/html")
            email_to_mentor.send()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cprofiles:mentor-profiles-list')




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class ConnectionListView(ListView):
    model = Connection
    template_name = 'choice/choice-connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all().order_by('-created')
        return qs

    

@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class ConnectionDetailView(DetailView):
    model = Connection
    template_name = 'choice/choice-connection-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        connection = Connection.objects.get(pk=pk)
        return connection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        connection = Connection.objects.get(pk=pk)
        sessions = Session.objects.filter(submit_status=True).filter(connection=connection)
        sessions_ = []
        for item in sessions:
            sessions_.append(item)
        context["sessions"] = sessions_
        return context



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def remove_connection(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        mentor_pk = request.POST.get('mentor_pk')
        student = Student.objects.get(pk=student_pk)
        mentor = Mentor.objects.get(pk=mentor_pk)

        rel = Connection.objects.get(Q(student=student), Q(mentor=mentor))
        rel.status = 'disconnected'
        rel.save()

        email_list = []
        email_list.append(student.email)
        email_list.append(mentor.email)
        email_list.append(student.parent1_email)

        program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))

        email_list.extend(program_manager_email_list)

        html_content = render_to_string("choice/disconnection-email.html", {'student': student, 'mentor': mentor })
        text_context = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Mentor/Student Disconnection ",
            text_context,
            'Choice Program - Peninsula Bridge',
            email_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cprofiles:mentor-profiles-list')




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def show_task_form(request, pk):

    tasksubjects = Tasksubject.objects.all()
    task = Task.objects.get(pk=pk)

    context = {'tasksubjects':tasksubjects,
                'task': task
                }

    return render(request, 'choice/show-task-form.html', context)




class TaskUpdateView(UpdateView):

    form_class = TaskModelForm
    model = Task
    template_name = 'choice/task-form.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasksubjects = Tasksubject.objects.all()
        tasksubjects_ = []
        for item in tasksubjects:
            tasksubjects_.append(item)
        context["tasksubjects"] = tasksubjects_
        return context


@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def generate_session_form(request):
    
    active_connection = Connection.objects.exclude(status='disconnected')

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("https://www.admin.peninsulabridge.org/choice/" + session_generated_pk + "/submit-feedback/")

        email_list = []
        email_list.append(x.mentor.email)

        form_link = "https://www.admin.peninsulabridge.org/choice/" + session_generated_pk + "/submit-feedback/"

        html_content = render_to_string("choice/choice-mentor-feedback-form.email.html", {'connection': x, 'form_link': form_link})
        text_context = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Choice Mentor Feedback Form",
            text_context,
            'Choice Program - Peninsula Bridge',
            email_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()


    g = []
    for y in active_connection:
        parentsession_generated = Parentsession.objects.create(connection=y)
        parentsession_generated_pk = str(parentsession_generated.pk)
        g.append("https://www.admin.peninsulabridge.org/choice/" + parentsession_generated_pk + "/submit-parent-feedback/")

        email_list = []
        email_list.append(x.student.parent1_email)

        form_link = "https://www.admin.peninsulabridge.org/choice/" + parentsession_generated_pk + "/submit-parent-feedback/"

        html_content = render_to_string("choice/choice-parent-feedback-form.html", {'connection': x, 'form_link': form_link})
        text_context = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Feedback Form // Forma de Comentarios",
            text_context,
            'Choice Program - Peninsula Bridge',
            email_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

    context = {'z':z,
               'g':g}

    return render(request, 'choice/choice-session-form-link.html', context)




def update_session(request, pk):

    session = Session.objects.get(pk=pk)
    form = SessionModelForm(instance=session)

    connection = Connection.objects.get(session__pk=pk)
    task = Task.objects.get(connection=connection)

    if request.method == 'POST':

        form = SessionModelForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('cprofiles:task-form', task)

    context = {'form':form,
                'session': session,

                }
    return render(request, 'choice/choice-submit-session-feedback.html', context)




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class SessionListView(ListView):
    model = Session
    template_name = 'choice/choice-session-list.html'

    def get_queryset(self):
        qs = Session.objects.filter(submit_status=True).order_by('-updated')
        return qs



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class SessionDetailView(DetailView):
    model = Session
    template_name = 'choice/choice-session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasksubjects = Tasksubject.objects.all()
        tasksubjects_ = []
        for item in tasksubjects:
            tasksubjects_.append(item)
        context["tasksubjects"] = tasksubjects_
        return context




def mentor_profile_form(request):

    form = MentorModelForm()

    if request.method == 'POST':
        form = MentorModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your interest in the Peninsula Bridge Choice Program! We will reach out to you over email when you are connected with a student.')
  
    context = {'form':form}

    return render(request, 'choice/mentor-profile-form.html', context)



def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your interest in the Peninsula Bridge Choice Program! We will reach out to you over email when you are connected with a mentor. ')
  
    context = {'form':form}

    return render(request, 'choice/choice-student-profile-form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def dashboard(request):

    # First Row

    high_student_count = Student.objects.filter(grade='8').count()
    middle_student_count = Student.objects.filter(grade='5').count()
    off_track_conn = Connection.objects.filter(progress='off track').count()
    total_connection = Connection.objects.all().count()

    # Second Row

    avg_rate = Session.objects.filter(submit_status=True).aggregate(Avg('rate'))
    hour_session = Session.objects.filter(submit_status=True).aggregate(Sum('length'))
    inactive_conn = Connection.objects.filter(status='inactive').count()
    unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

    # Third Row

    on_track_conn = Connection.objects.filter(progress='on track').count()
    total_conn = Connection.objects.all().count()

    if total_conn == 0:
        on_track_conn_percentage = 0
    else:
        on_track_conn_percentage = on_track_conn/total_conn * 100
    
    other_conn_percentage = 100 - on_track_conn_percentage
    
    z = []
    for session in Session.objects.filter():
        z.append(list(session.get_topics().values('name')))   

    flat_list = [item for sublist in z for item in sublist]
    unique_counts = dict(collections.Counter(e['name'] for e in flat_list))

    # Fourth Row

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
    avg_eng_prod_month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(rate=Avg('rate')).annotate(prod=Avg('productivity'))

    
    # Fifth Row
    
    this_year = datetime.now().year

    #Teacher recommendation
    tr = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Teacher recommendation').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    tr_list = []
    for l in tr:
        for c, m in l.items():
            tr_list.append(m)

    tr_dict = dict(zip(tr_list[::2], tr_list[1::2]))

    tr_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in tr_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            tr_dict.setdefault(mmyyyy, 0)

    tr_dict = dict(sorted(tr_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    tr_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in tr_dict.items()}

    # Creating a Ravenna account
    cr = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Creating a Ravenna account').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    cr_list = []
    for l in cr:
        for c, m in l.items():
            cr_list.append(m)

    cr_dict = dict(zip(cr_list[::2], cr_list[1::2]))

    cr_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in cr_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            cr_dict.setdefault(mmyyyy, 0)

    cr_dict = dict(sorted(cr_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    cr_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in cr_dict.items()}


    # Interview preparation
    ip = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Interview preparation').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    ip_list = []
    for l in ip:
        for c, m in l.items():
            ip_list.append(m)

    ip_dict = dict(zip(ip_list[::2], ip_list[1::2]))

    ip_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in ip_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            ip_dict.setdefault(mmyyyy, 0)

    ip_dict = dict(sorted(ip_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    ip_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in ip_dict.items()}


    # Shadow day preparation
    sd = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Shadow day preparation').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    sd_list = []
    for l in sd:
        for c, m in l.items():
            sd_list.append(m)

    sd_dict = dict(zip(sd_list[::2], sd_list[1::2]))

    sd_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in sd_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            sd_dict.setdefault(mmyyyy, 0)

    sd_dict = dict(sorted(sd_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    sd_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in sd_dict.items()}

    # Essays
    es = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Essays').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    es_list = []
    for l in es:
        for c, m in l.items():
            es_list.append(m)

    es_dict = dict(zip(es_list[::2], es_list[1::2]))

    es_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in es_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            es_dict.setdefault(mmyyyy, 0)

    es_dict = dict(sorted(es_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    es_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in es_dict.items()}

    # Test prep
    tp = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Test prep').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    tp_list = []
    for l in tp:
        for c, m in l.items():
            tp_list.append(m)

    tp_dict = dict(zip(tp_list[::2], tp_list[1::2]))

    tp_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in tp_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            tp_dict.setdefault(mmyyyy, 0)

    tp_dict = dict(sorted(tp_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    tp_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in tp_dict.items()}

    # Filling out application
    fp = Topiccalculation.objects.filter(updated__year=this_year).filter(name='Filling out application').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    fp_list = []
    for l in fp:
        for c, m in l.items():
            fp_list.append(m)

    fp_dict = dict(zip(fp_list[::2], fp_list[1::2]))

    fp_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in fp_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            fp_dict.setdefault(mmyyyy, 0)

    fp_dict = dict(sorted(fp_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    fp_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in fp_dict.items()}

    # Sixth Row

    recent_session = Session.objects.filter(submit_status=True).order_by('-created')[:5]

 
    context = {'month':month,
                'unique_counts':unique_counts,
                'recent_session':recent_session,
                'on_track_conn_percentage': on_track_conn_percentage,
                'other_conn_percentage': other_conn_percentage,
                'high_student_count': high_student_count,
                'middle_student_count': middle_student_count,
                'off_track_conn':  off_track_conn,
                'avg_rate': avg_rate,
                'hour_session': hour_session,
                'inactive_conn': inactive_conn,
                'total_connection': total_connection,
                'unanswered_question_num': unanswered_question_num,
                'avg_eng_prod_month': avg_eng_prod_month,
                'tr_dict': tr_dict,
                'cr_dict': cr_dict,
                'ip_dict': ip_dict,
                'sd_dict': sd_dict,
                'es_dict': es_dict,
                'tp_dict': tp_dict,
                'fp_dict': fp_dict,

                }

    return render(request, 'choice/choice-dashboard.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def check_connection_status(request):

    todays_date = timezone.now()
    four_weeks_ago = todays_date-timedelta(days=28)

    active_connection = Connection.objects.filter(status='connected')

    inactive_list = [0, 0, 0, 0]

    for x in active_connection:
        for y in x.get_all_sessions():
            if y.updated >= four_weeks_ago:
                break
            else:
                x.status = 'inactive'
                x.flag = True
                x.save()
                email_list = []
                email_list.append(x.student.email)
                email_list.append(x.student.parent1_email)
                email_list.append(x.mentor.email)
                program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
                email_list.extend(program_manager_email_list)

                html_content = render_to_string("choice/connection-inactive-email.html", {'connection': x})
                text_context = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    "Choice Program: Inactive Mentor/Student Relationship",
                    text_context,
                    'Choice Program - Peninsula Bridge',
                    email_list,
                )

                email.attach_alternative(html_content, "text/html")
                email.send()

                break
  
        list_meet = []
        for y in x.get_all_sessions_four():
            list_meet.append(y.meet)

        if list_meet == inactive_list:
            x.status = 'inactive'
            x.flag = True
            x.save()
            email_list = []
            email_list.append(x.student.email)
            email_list.append(x.student.parent1_email)
            email_list.append(x.mentor.email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='choice').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("choice/connection-inactive-email.html", {'connection': x})
            text_context = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Choice Program: Inactive Mentor/Student Relationship",
                text_context,
                'Choice Program - Peninsula Bridge',
                email_list,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

    return HttpResponse("Connection Status Checked")




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def flag_unflag_connection(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        connection_obj = Connection.objects.get(id=post_id)

        if connection_obj.flag == False:
            Connection.objects.filter(id=post_id).update(flag=True)


        else:
            Connection.objects.filter(id=post_id).update(flag=False)


        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def flag_unflag_student(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        student_obj = Student.objects.get(id=post_id)

        if student_obj.flag == False:
            Student.objects.filter(id=post_id).update(flag=True)


        else:
            Student.objects.filter(id=post_id).update(flag=False)


        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')


@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def flag_unflag_mentor(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        mentor_obj = Mentor.objects.get(id=post_id)

        if mentor_obj.flag == False:
            Mentor.objects.filter(id=post_id).update(flag=True)


        else:
            Mentor.objects.filter(id=post_id).update(flag=False)


        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def flag_unflag_session(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        session_obj = Session.objects.get(id=post_id)

        if session_obj.flag == False:
            Session.objects.filter(id=post_id).update(flag=True)


        else:
            Session.objects.filter(id=post_id).update(flag=False)

        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'choice/question-list.html'

    def get_queryset(self):
        qs = Question.objects.all().order_by('status').reverse()
        return qs


@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def action_question(request):
    if request.method == 'POST':

        post_id = request.POST.get('post_id')
        question_obj = Question.objects.get(id=post_id)

        if question_obj.action == False:
            Question.objects.filter(id=post_id).update(action=True, status='ADDRESSED')

        else:
            Question.objects.filter(id=post_id).update(action=False, status='UNANSWERED')


        data = {

        }

        return JsonResponse(data, safe=False)
    return redirect('cprofiles:dashboard')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class ParentSessionListView(ListView):
    model = Parentsession
    template_name = 'choice/parent-session-list.html'

    def get_queryset(self):
        qs = Parentsession.objects.filter(submit_status=True).order_by('-updated')
        return qs



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def flag_unflag_parent_session(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        session_obj = Parentsession.objects.get(id=post_id)

        if session_obj.flag == False:
            Parentsession.objects.filter(id=post_id).update(flag=True)

        else:
            Parentsession.objects.filter(id=post_id).update(flag=False)

        

        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('cprofiles:dashboard')




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class ParentSessionDetailView(DetailView):
    model = Session
    template_name = 'choice/parent-session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        parentsession = Parentsession.objects.get(pk=pk)
        return parentsession



class ParentSessionUpdateView(UpdateView):
    form_class = ParentSessionModelForm
    model = Parentsession
    template_name = 'choice/submit-parent-session-feedback.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_object(self):
        pk = self.kwargs.get('pk')
        parentsession = Parentsession.objects.get(pk=pk)
        return parentsession

    def form_valid(self, form):
        self.object.submit_status = True
        self.object = form.save()
        return redirect('profiles:session-submitted')




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])	
def search_connection(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        qs = Connection.objects.all().order_by('-created').filter(status=status)

    context = {'qs':qs}

    return render(request, 'choice/connection-list-search.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def export_choice_mentor_list(request):

    mentors = Mentor.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=choice_mentor_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'avatar', 'prefer_grade', 'prefer_gender', 'prefer_location', 'mentor_last_year', 'language', 
    'experience', 'familiar', 'share', 'hobby', 'question', 'student', 'date_added', 'flag'])
    
    for q in mentors:
        writer.writerow([q.id, q.first_name, q.last_name, q.email, q.phone, q.address, q.avatar, q.prefer_grade, q.prefer_gender, 
        '|'.join(c.name for c in q.prefer_location.all()), q.mentor_last_year, '|'.join(c.name for c in q.language.all()),
        q.experience, q.familiar, q.share, q.hobby, q.question, '|'.join(c.first_name + ' ' + c.last_name for c in q.friends.all()), 
        q.created, q.flag])
    return response





@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def export_choice_student_list(request):

    students = Student.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=choice_student_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'email', 'gender', 'grade', 'school', 'language_preference', 
    'parent1_first_name', 'parent1_last_name', 'parent1_phone', 'parent1_email', 'activity', 'ind_scl', 
    'dont_know', 'proud', 'learn', 'happy', 'hobby', 'int_ind_school', 'look_ind_school', 'strength', 
    'obstacle', 'child_strength', 'social_strength', 'interview_language', 'question', 'mentor', 'date_added', 'flag'])
    
    for q in students:
        writer.writerow([q.id, q.first_name, q.last_name, q.email, q.gender, q.grade, q.school, q.language_preference, 
    q.parent1_first_name, q.parent1_last_name, q.parent1_phone, q.parent1_email, q.activity, q.ind_scl, 
    q.dont_know, q.proud, q.learn, q.happy, q.hobby, q.int_ind_school, q.look_ind_school, q.strength, 
    q.obstacle, '|'.join(c.name for c in q.child_strength.all()), '|'.join(c.name for c in q.social_strength.all()), q.interview_language, q.question,
    '|'.join(c.first_name + ' ' + c.last_name for c in q.get_friends()), q.created, q.flag])
    return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def export_choice_connection_list(request):

    connections = Connection.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=choice_connection_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'created', 'student', 'mentor', 'status', 'updated', 'flag', 'progress'])
    
    for q in connections:
        writer.writerow([q.id, q.created, q.student.first_name + ' ' + q.student.last_name,
        q.mentor.first_name + ' ' + q.mentor.last_name, q.status, q.updated, q.flag, q.progress])
        
    return response



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def export_choice_session_list(request):

    sessions = Session.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=choice_session_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'connection', 'meet', 'length', 'topic', 'updated', 'created', 'feedback', 'change', 'support', 
    'elaborate', 'rate', 'productivity', 'question', 'submit_status', 'step', 'flag' ])
    
    for q in sessions:
        writer.writerow([q.id, q.connection, q.meet, q.length, '|'.join(c.name for c in q.topic.all()), q.updated,
        q.created, q.feedback, q.change, '|'.join(c.name for c in q.support.all()), q.elaborate, 
        q.rate, q.productivity, q.question, q.submit_status, q.step, q.flag])
        
    return response




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class ParentSessionSpanishUpdateView(UpdateView):
    form_class = ParentSessionModelForm
    model = Parentsession
    template_name = 'choice/submit-parent-session-feedback-spanish.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_object(self):
        pk = self.kwargs.get('pk')
        parentsession = Parentsession.objects.get(pk=pk)
        return parentsession

    def form_valid(self, form):
        self.object.submit_status = True
        self.object = form.save()
        return redirect('profiles:session-submitted')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['choice', 'admin']), name='dispatch')
class StudentNoteUpdateView(UpdateView):
    form_class = StudentNoteModelForm
    model = Student
    template_name = 'choice/note-update.html'

    def get_success_url(self):
        return reverse("cprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})





@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class ConnectionNoteUpdateView(UpdateView):
    form_class = ConnectionNoteModelForm
    model = Connection
    template_name = 'choice/note-update.html'

    def get_success_url(self):
        return reverse("cprofiles:connection-profile-detail", kwargs={"pk": self.object.pk})


from datetime import datetime, timedelta



@login_required(login_url='login')
@allowed_users(allowed_roles=['choice', 'admin'])
def feedback_form_status(request):

    active_connection = Connection.objects.filter(status='connected')

    try:
        latest_session = Session.objects.latest('created')
    except Session.DoesNotExist:
        latest_session = None

    if latest_session:
        now = latest_session.created
        monday = now - timedelta(days = now.weekday())
        last_monday = monday - timedelta(days=14)
        last_last_monday = monday - timedelta(days=28)

    else:
        monday = None
        last_monday = None
        last_last_monday = None

    context = {'active_connection':active_connection,
                'monday': monday,
                'last_monday': last_monday,
                'last_last_monday': last_last_monday,
                }

    return render(request, 'choice/feedback-form-status.html', context)