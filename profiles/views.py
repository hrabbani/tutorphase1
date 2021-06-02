from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Connection, Session, Subject
from .forms import SessionModelForm, TutorModelForm, StudentModelForm
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
from django.core.mail import send_mail
from core.decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
from django.contrib import messages




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
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



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
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



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
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
        sessions = Session.objects.filter(submit_status=True).filter(Q(connection__tutor=profile) | Q(connection__student=profile))
        sessions_ = []
        for item in sessions:
            sessions_.append(item)
        context["sessions"] = sessions_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class TutorUpdateView(UpdateView):
    form_class = TutorModelForm
    model = Profile
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.object.slug})



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class StudentUpdateView(UpdateView):
    form_class = StudentModelForm
    model = Profile
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.object.slug})



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class TutorProfileListView(ListView):
    model = Profile
    template_name = 'tutor-profile-list.html'

    def get_queryset(self):
        qs = Profile.objects.filter(role='tutor')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipients = list(i for i in Profile.objects.filter(role='tutor').values_list('email', flat=True))
        recipients = ("; ".join(recipients))
        context["recipients"] = recipients
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class StudentProfileListView(ListView):
    model = Profile
    template_name = 'student-profile-list.html'

    def get_queryset(self):
        qs = Profile.objects.filter(role='student')
        return qs


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def tutor_connect(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        tutor_pk = request.POST.get('tutor_pk')
        student = Profile.objects.get(pk=student_pk)
        tutor = Profile.objects.get(pk=tutor_pk)

        # subject_list = list(student.get_subjects().values('name'))
        # subject_list = [d['name'] for d in subject_list]
        # subject_list = ", ".join(subject_list)

        exist_connection = Connection.objects.filter(student=student).filter(tutor=tutor)

        if exist_connection.exists():
            exist_connection = Connection.objects.get(Q(student=student), Q(tutor=tutor))
            exist_connection.status = 'connected'
            exist_connection.save()

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.parent2_email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Tutor" + " " + tutor.first_name + " " + tutor.last_name

            send_mail('Connection Established',
            content,
            'Student-Tutor Program',
            email_list,
            fail_silently=False
            )


        else:
            rel = Connection.objects.create(student=student, tutor=tutor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.parent2_email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student" + student.first_name + student.last_name + "Tutor" + tutor.first_name + tutor.last_name

            send_mail('Connection Established',
            content,
            'Student-Tutor Program',
            email_list,
            fail_silently=False
            )



        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def student_connect(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        tutor_pk = request.POST.get('tutor_pk')
        student = Profile.objects.get(pk=student_pk)
        tutor = Profile.objects.get(pk=tutor_pk)

        # subject_list = list(tutor.get_subjects().values('name'))
        # subject_list = [d['name'] for d in subject_list]
        # subject_list = ", ".join(subject_list)

        exist_connection = Connection.objects.filter(student=student).filter(tutor=tutor)

        if exist_connection.exists():
            exist_connection = Connection.objects.get(Q(student=student), Q(tutor=tutor))
            exist_connection.status = 'connected'
            exist_connection.save()

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.parent2_email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Tutor" + " " + tutor.first_name + " " + tutor.last_name

            send_mail('Connection Established',
            content,
            'Student-Tutor Program',
            email_list,
            fail_silently=False
            )


        else:
            rel = Connection.objects.create(student=student, tutor=tutor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.parent2_email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Tutor" + " " + tutor.first_name + " " + tutor.last_name

            send_mail('Connection Established',
            content,
            'Student-Tutor Program',
            email_list,
            fail_silently=False
            )


        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ConnectionListView(ListView):
    model = Connection
    template_name = 'connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all().order_by('-created')
        return qs




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ConnectionDetailView(DetailView):
    model = Connection
    template_name = 'connection-detail.html'

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
@allowed_users(allowed_roles=['tutor', 'admin'])	
def remove_connection(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        tutor_pk = request.POST.get('tutor_pk')
        student = Profile.objects.get(pk=student_pk)
        tutor = Profile.objects.get(pk=tutor_pk)

        rel = Connection.objects.get(Q(student=student), Q(tutor=tutor))
        rel.status = 'disconnected'
        rel.save()

        email_list = []
        email_list.append(student.email)
        email_list.append(tutor.email)
        email_list.append(student.parent1_email)
        email_list.append(student.parent2_email)
        email_list.append(student.academic_advisor_email)

        program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))

        email_list.extend(program_manager_email_list)

        content = "Connection is disconnected between Student " + student.first_name + " " + student.last_name + " " + "Tutor" + " " + tutor.first_name + " " + tutor.last_name

        send_mail('Connection Disconnected',
        content,
        'Student-Tutor Program',
        email_list,
        fail_silently=False
        )
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class SessionListView(ListView):
    model = Session
    template_name = 'session-list.html'

    def get_queryset(self):
        qs = Session.objects.filter(submit_status=True).order_by('-created')
        return qs




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class SessionDetailView(DetailView):
    model = Session
    template_name = 'session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def generate_session_form(request):
    
    active_connection = Connection.objects.filter(status='connected')

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("http://127.0.0.1:8000/profiles/" + session_generated_pk + "/submit-feedback/")

        email = x.tutor.email

        content = "http://127.0.0.1:8000/profiles/" + session_generated_pk + "/submit-feedback/"

        send_mail('Please fill in the Session Feedback Form',
        content,
        'Student-Tutor Program',
        [email],
        fail_silently=False
        )

    context = {'z':z}

    return render(request, 'session-form-link.html', context)

    


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class SessionUpdateView(UpdateView):
    form_class = SessionModelForm
    model = Session
    template_name = 'submit-session-feedback.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session

    def form_valid(self, form):
        self.object.submit_status = True
        self.object = form.save()
        return super().form_valid(form)


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def session_submitted(request):

    return render(request, 'session-submitted.html')



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def tutor_profile_form(request):

    form = TutorModelForm()

    if request.method == 'POST':
        form = TutorModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'tutor'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Tutor Profile Added')
  
    context = {'form':form}

    return render(request, 'tutor-profile-form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'student'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Student Profile Added')
  
    context = {'form':form}

    return render(request, 'student-profile-form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
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
    thirty_days_session = Session.objects.filter(submit_status=True).filter(created__gte=thirty_days_ago, created__lte=todays_date)

    num_session = thirty_days_session.count()
    hour_session = thirty_days_session.aggregate(Sum('length'))
  
    num_math = thirty_days_session.filter(subjects__in=[1]).count()
    num_english = thirty_days_session.filter(subjects__in=[2]).count()

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
    recent_session = Session.objects.filter(submit_status=True).order_by('-created')[:5]

    z = []
    for session in Session.objects.filter():
        z.append(list(session.get_subjects().values('name')))   

    flat_list = [item for sublist in z for item in sublist]
    unique_counts = dict(collections.Counter(e['name'] for e in flat_list))


    num_tutor = Profile.objects.filter(role='tutor').count()

    avg_rate = Session.objects.filter(submit_status=True).aggregate(Avg('rate'))

    inactive_conn = Connection.objects.filter(status='inactive').count()

    connected_conn = Connection.objects.filter(status='connected').count()

    context = {'month':month,
                'x':x,
                'y':y,
                'num_session':num_session,
                'hour_session':hour_session,
                'num_math':num_math,
                'num_english':num_english,
                'recent_session':recent_session,
                'unique_counts':unique_counts,
                'num_tutor': num_tutor,
                'avg_rate': avg_rate,
                'inactive_conn': inactive_conn,
                'connected_conn': connected_conn,
                }

    return render(request, 'dashboard.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def like_unlike_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        student_obj = Profile.objects.get(id=post_id)

        if student_obj.flag == False:
            Profile.objects.filter(id=post_id).update(flag=True)

        else:
            Profile.objects.filter(id=post_id).update(flag=False)

        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')




@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
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
@allowed_users(allowed_roles=['tutor', 'admin'])	
def flag_unflag_tutor(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        tutor_obj = Profile.objects.get(id=post_id)

        if tutor_obj.flag == False:
            Profile.objects.filter(id=post_id).update(flag=True)

        else:
            Profile.objects.filter(id=post_id).update(flag=False)

        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def search_connection(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        qs = Connection.objects.all().order_by('-created').filter(status=status)

    context = {'qs':qs}

    return render(request, 'connection-list-search.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def check_connection_status(request):

    todays_date = timezone.now()
    three_weeks_ago = todays_date-timedelta(days=21)

    active_connection = Connection.objects.filter(status='connected')

    inactive_list = [0, 0, 0]

    for x in active_connection:
        for y in x.get_all_sessions():
            if y.updated >= three_weeks_ago:
                break
            else:
                x.status = 'inactive'
                x.flag = True
                x.save()
                email_list = []
                email_list.append(x.student.academic_advisor_email)
                program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
                email_list.extend(program_manager_email_list)

                content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.tutor.first_name + " " + x.tutor.last_name + " " + "because no session feedback form was submitted for three weeks straight"

                send_mail('Connection Inactive',
                content,
                'Student-Tutor Program',
                email_list,
                fail_silently=False
                )

                break
  
        list_meet = []
        for y in x.get_all_sessions_three():
            list_meet.append(y.meet)

        if list_meet == inactive_list:
            x.status = 'inactive'
            x.flag = True
            x.save()
            email_list = []
            email_list.append(x.student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.tutor.first_name + " " + x.tutor.last_name + " " + "because 'Zero' Meets were submitted in Session Feedback form for three sessions straight."

            send_mail('Connection Inactive',
            content,
            'Student-Tutor Program',
            email_list,
            fail_silently=False
            )

    return HttpResponse("Connection Status Checked")


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def table(request):

    return render(request, 'table.html')




