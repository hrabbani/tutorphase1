from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Connection, Session, Subject
from .forms import ProfileModelForm
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




class TutorProfileDetailView(DetailView):
    model = Profile
    template_name = 'tutor-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Profile.objects.filter(role='student')
        students_ = []
        for item in students:
            students_.append(item)
        context["students"] = students_
        return context


class StudentProfileDetailView(DetailView):
    model = Profile
    template_name = 'student-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutors = Profile.objects.filter(role='tutor')
        tutors_ = []
        for item in tutors:
            tutors_.append(item)
        context["tutors"] = tutors_
        return context



class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile-detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        sessions = Session.objects.filter(Q(connection__tutor=profile) | Q(connection__student=profile))
        sessions_ = []
        for item in sessions:
            sessions_.append(item)
        context["sessions"] = sessions_
        return context


class TutorProfileListView(ListView):
    model = Profile
    template_name = 'tutor-profile-list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.filter(role='tutor')
        return qs



class StudentProfileListView(ListView):
    model = Profile
    template_name = 'student-profile-list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.filter(role='student')
        return qs


def connect(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        tutor_pk = request.POST.get('tutor_pk')
        student = Profile.objects.get(pk=student_pk)
        tutor = Profile.objects.get(pk=tutor_pk)

        exist_connection = Connection.objects.filter(student=student).filter(tutor=tutor)

        if exist_connection.exists():
            exist_connection = Connection.objects.get(Q(student=student), Q(tutor=tutor))
            exist_connection.status = 'connected'
            exist_connection.save()
        else:
            rel = Connection.objects.create(student=student, tutor=tutor, status='connected')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')



class ConnectionListView(ListView):
    model = Connection
    template_name = 'connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all()
        return qs


def remove_connection(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        tutor_pk = request.POST.get('tutor_pk')
        student = Profile.objects.get(pk=student_pk)
        tutor = Profile.objects.get(pk=tutor_pk)

        rel = Connection.objects.get(Q(student=student), Q(tutor=tutor))
        rel.status = 'disconnected'
        rel.save()
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')



class SessionListView(ListView):
    model = Session
    template_name = 'session-list.html'

    def get_queryset(self):
        qs = Session.objects.all().order_by('-created')
        return qs



class SessionDetailView(DetailView):
    model = Session
    template_name = 'session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session



def tutor_profile_form(request):

    form = ProfileModelForm()

    if request.method == 'POST':
        form = ProfileModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'tutor'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Tutor Profile Added')
  
    context = {'form':form}

    return render(request, 'tutor-profile-form.html', context)



def student_profile_form(request):

    form = ProfileModelForm()

    if request.method == 'POST':
        form = ProfileModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'student'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Student Profile Added')
  
    context = {'form':form}

    return render(request, 'student-profile-form.html', context)




def dashboard(request):

    x = 0
    for tutor in Profile.objects.filter(role='tutor'):
        if tutor.get_friends_no() == 0:
            x = x + 1

    y = 0
    for student in Profile.objects.filter(role='student'):
        if student.get_friends_no() == 0:
            y = y + 1

    todays_date = timezone.now()
    thirty_days_ago = todays_date-timedelta(days=30)
    thirty_days_session = Session.objects.filter(created__gte=thirty_days_ago, created__lte=todays_date)

    num_session = thirty_days_session.count()
    hour_session = thirty_days_session.aggregate(Sum('length'))
  
    num_math = thirty_days_session.filter(subjects__in=[1]).count()
    num_english = thirty_days_session.filter(subjects__in=[2]).count()

    month = Session.objects.annotate(month=TruncMonth('created')).values('month').annotate(total=Count('connection'))
    recent_session = Session.objects.all().order_by('-created')[:5]

    z = []
    for session in Session.objects.filter():
        z.append(list(session.get_subjects().values('name')))

    flat_list = [item for sublist in z for item in sublist]
    unique_counts = dict(collections.Counter(e['name'] for e in flat_list))

    context = {'month':month,
                'x':x,
                'y':y,
                'num_session':num_session,
                'hour_session':hour_session,
                'num_math':num_math,
                'num_english':num_english,
                'recent_session':recent_session,
                'unique_counts':unique_counts,
                }

    return render(request, 'dashboard.html', context)