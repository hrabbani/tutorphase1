from django.template.defaultfilters import length
from cprofiles.models import Student, Mentor, Connection, Task, Tasksubject, Session
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mentor, Student
from .forms import TaskModelForm, SessionModelForm, MentorModelForm, StudentModelForm
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

def home_view(request):

    return render(request, 'cprofiles.html') 



class MentorProfileListView(ListView):
    model = Mentor
    template_name = 'mentor-profile-list.html'

    def get_queryset(self):
        qs = Mentor.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipients = list(i for i in Mentor.objects.values_list('email', flat=True))
        recipients = ("; ".join(recipients))
        context["recipients"] = recipients
        return context



class StudentProfileListView(ListView):
    model = Student
    template_name = 'choice-student-profile-list.html'

    def get_queryset(self):
        qs = Student.objects.all()
        return qs



class MentorDetailView(DetailView):
    model = Mentor
    template_name = 'mentor-detail.html'

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



class MentorUpdateView(UpdateView):
    form_class = MentorModelForm
    model = Mentor
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("cprofiles:mentor-profiles-detail", kwargs={"slug": self.object.slug})


class StudentUpdateView(UpdateView):
    form_class = StudentModelForm
    model = Student
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("cprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})



class StudentDetailView(DetailView):
    model = Student
    template_name = 'student-detail.html'

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




class MentorProfileDetailView(DetailView):
    model = Mentor
    template_name = 'mentor-connect.html'

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


class StudentProfileDetailView(DetailView):
    model = Student
    template_name = 'choice-student-connect.html'

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




def connect(request):
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
        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cprofiles:mentor-profiles-list')




class ConnectionListView(ListView):
    model = Connection
    template_name = 'choice-connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all().order_by('-created')
        return qs

    


class ConnectionDetailView(DetailView):
    model = Connection
    template_name = 'choice-connection-detail.html'

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



def remove_connection(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        mentor_pk = request.POST.get('mentor_pk')
        student = Student.objects.get(pk=student_pk)
        mentor = Mentor.objects.get(pk=mentor_pk)

        rel = Connection.objects.get(Q(student=student), Q(mentor=mentor))
        rel.status = 'disconnected'
        rel.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('cprofiles:mentor-profiles-list')




def show_task_form(request, pk):

    tasksubjects = Tasksubject.objects.all()

    print(tasksubjects)

    task = Task.objects.get(pk=pk)

    print(task)

    context = {'tasksubjects':tasksubjects,
                'task': task
                }

    return render(request, 'show-task-form.html', context)



class TaskUpdateView(UpdateView):

    form_class = TaskModelForm
    model = Task
    template_name = 'task-form.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasksubjects = Tasksubject.objects.all()
        tasksubjects_ = []
        for item in tasksubjects:
            tasksubjects_.append(item)
        context["tasksubjects"] = tasksubjects_
        return context


def generate_session_form(request):
    
    active_connection = Connection.objects.filter(status='connected')

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("http://127.0.0.1:8000/cprofiles/" + session_generated_pk + "/submit-feedback/")


    context = {'z':z}

    return render(request, 'choice-session-form-link.html', context)





def update_session(request, pk):

    session = Session.objects.get(pk=pk)
    form = SessionModelForm(instance=session)

    connection = Connection.objects.get(session__pk=pk)
    task = Task.objects.get(connection=connection)

    if request.method == 'POST':

        form = SessionModelForm(request.POST, instance=session)
        if form.is_valid():
            new_status = form.save(commit=False)
            new_status.submit_status = True
            new_status.save()
            form.save_m2m()
            return redirect('cprofiles:task-form', task)

    context = {'form':form,
                'session': session,

                }
    return render(request, 'choice-submit-session-feedback.html', context)



class SessionListView(ListView):
    model = Session
    template_name = 'choice-session-list.html'

    def get_queryset(self):
        qs = Session.objects.filter(submit_status=True).order_by('-updated')
        return qs



class SessionDetailView(DetailView):
    model = Session
    template_name = 'choice-session-detail.html'

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
            return HttpResponse('Mentor Profile Added')
  
    context = {'form':form}

    return render(request, 'mentor-profile-form.html', context)



def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Student Profile Added')
  
    context = {'form':form}

    return render(request, 'choice-student-profile-form.html', context)


def dashboard(request):

    high_student_count = Student.objects.filter(grade='8').count()
    
    middle_student_count = Student.objects.filter(grade='5').count()

    off_track_conn = Connection.objects.filter(progress='off track').count()

    inactive_conn = Connection.objects.filter(status='inactive').count()

    hour_session = Session.objects.filter(submit_status=True).aggregate(Sum('length'))

    avg_rate = Session.objects.filter(submit_status=True).aggregate(Avg('rate'))

    on_track_conn = Connection.objects.filter(progress='on track').count()

    total_conn = Connection.objects.all().count()

    on_track_conn_percentage = on_track_conn/total_conn * 100

    other_conn_percentage = 100 - on_track_conn_percentage

    print(on_track_conn)
    
    z = []
    for session in Session.objects.filter():
        z.append(list(session.get_topics().values('name')))   

    flat_list = [item for sublist in z for item in sublist]
    unique_counts = dict(collections.Counter(e['name'] for e in flat_list))

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
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
                'inactive_conn': inactive_conn

                }

    return render(request, 'choice-dashboard.html', context)