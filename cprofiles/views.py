from django.template.defaultfilters import length
from cprofiles.models import Student, Mentor, Connection, Task, Tasksubject, Session
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mentor, Student
from .forms import TaskModelForm, SessionModelForm
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
import json
from datetime import timedelta
from datetime import date
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
import collections
from django.urls import reverse_lazy
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     sessions = Session.objects.filter(submit_status=True).filter(Q(connection__tutor=profile) | Q(connection__student=profile))
    #     sessions_ = []
    #     for item in sessions:
    #         sessions_.append(item)
    #     context["sessions"] = sessions_
    #     return context


class StudentDetailView(DetailView):
    model = Student
    template_name = 'student-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        mentor = Student.objects.get(slug=slug)
        return mentor

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     sessions = Session.objects.filter(submit_status=True).filter(Q(connection__tutor=profile) | Q(connection__student=profile))
    #     sessions_ = []
    #     for item in sessions:
    #         sessions_.append(item)
    #     context["sessions"] = sessions_
    #     return context




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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_date = datetime.date.today()
        tasks = Task.objects.all()

        for task in tasks:
            task.progress = 'on track'
            task.save()
            task.connection.flag = False
            task.connection.save()
            if task.task1status == None:
                task.progress = None
                task.save()
            if task.task1status == 'not completed':
                try:
                    if task.tasksubject.all()[0].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task2status == 'not completed':
                try:
                    if task.tasksubject.all()[1].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task3status == 'not completed':
                try:
                    if task.tasksubject.all()[2].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task4status == 'not completed':
                try:
                    if task.tasksubject.all()[3].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task5status == 'not completed':
                try:
                    if task.tasksubject.all()[4].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task6status == 'not completed':
                try:
                    if task.tasksubject.all()[5].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task7status == 'not completed':
                try:
                    if task.tasksubject.all()[6].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task8status == 'not completed':
                try:
                    if task.tasksubject.all()[7].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task9status == 'not completed':
                try:
                    if task.tasksubject.all()[8].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass
            if task.task10status == 'not completed':
                try:
                    if task.tasksubject.all()[9].duedate < today_date:
                        task.progress = 'off track'
                        task.save()
                        task.connection.flag = True
                        task.connection.save()
                except:
                    pass

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


# def task_form(request):

#     form = TaskModelForm()

#     if request.method == 'POST':
#         form = ProfileModelForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             new_role = form.save(commit=False)
#             new_role.role = 'student'
#             new_role.save()
#             form.save_m2m()
#             return HttpResponse('Student Profile Added')
  
#     context = {'form':form}

#     return render(request, 'task-form.html', context)


# class TaskUpdateView(UpdateView):

#     form_class = TaskModelForm
#     model = Task
#     template_name = 'task-form.html'
#     success_url = reverse_lazy('cprofiles:connection-list')

#     def get_object(self):
#         pk = self.kwargs.get('pk')
#         session = Task.objects.get(pk=pk)
#         return session


# def deadline(request):

#     todays_date = timezone.now()
#     print(todays_date)
#     a = Task.objects.filter(Q(task1date__lte=todays_date)|Q(task2date__lte=todays_date)).filter(Q(task1status='not completed')|Q(task2status='not completed'))

#     print(a)

#     return HttpResponse("hihi")




# class ConnectionListView(ListView):
#     model = Connection
#     template_name = 'choice-connection-list.html'

#     def get_queryset(self):
#         qs = Connection.objects.all().order_by('-created')
#         return qs


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         today_date = datetime.date.today()

#         for task in Task.objects.all():
#             if task.task1date:
#                 if task.task1date < today_date:
#                     if task.task1status == 'not completed':
#                         task.progress = 'off track'
#                         task.save()
#                     else:
#                         task.progress = 'on track'
#                         task.save()
#             if task.task2date:
#                 if task.task2date < today_date:
#                     if task.task2status == 'not completed':
#                         task.progress = 'off track'
#                         task.save()
#                     else:
#                         task.progress = 'on track'
#                         task.save()  

#         return context




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

    print(task)
    print(connection)

    if request.method == 'POST':

        form = SessionModelForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('cprofiles:task-form', task)

    context = {'form':form,
                'session': session,

                }
    return render(request, 'choice-submit-session-feedback.html', context)

