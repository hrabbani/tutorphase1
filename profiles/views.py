from functools import total_ordering
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Connection, Session, Subject, Subjectcalculation, Question
from .forms import SessionModelForm, TutorModelForm, StudentModelForm, ProfileNoteModelForm, ConnectionNoteModelForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
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
from collections import defaultdict
from datetime import datetime
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import csv
import time


connection = get_connection(host='smtp.gmail.com', 
                                port=587, 
                                username='hstutoring@peninsulabridge.org', 
                                password='bridge89', 
                                use_tls=True)


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class TutorProfileDetailView(DetailView):
    model = Profile
    template_name = 'tutor/tutor-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Profile.objects.filter(role='student', status='active')
        students_ = []
        for item in students:
            students_.append(item)
        context["students"] = students_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class StudentProfileDetailView(DetailView):
    model = Profile
    template_name = 'tutor/student-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tutors = Profile.objects.filter(role='tutor', status='active')
        tutors_ = []
        for item in tutors:
            tutors_.append(item)
        context["tutors"] = tutors_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'tutor/profile-detail.html'

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
    template_name = 'tutor/tutor-profile-list.html'

    def get_queryset(self):
        qs = Profile.objects.filter(role='tutor')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_recipients = []
        active_conn = Connection.objects.filter(status='connected')

        for i in active_conn:
            active_recipients.append(i.tutor.email)

        active_recipients = list(set(active_recipients))
        active_recipients = ("; ".join(active_recipients))
        context["active_recipients"] = active_recipients

        recipients = list(i for i in Profile.objects.filter(role='tutor').values_list('email', flat=True))
        recipients = ("; ".join(recipients))
        context["recipients"] = recipients
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class StudentProfileListView(ListView):
    model = Profile
    template_name = 'tutor/student-profile-list.html'

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

        global connection


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
            email_list.append(student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("tutor/connection-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "Peninsula Bridge: Tutoring Connection Established | Conexión de Tutoría!",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection,
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()

        else:
            rel = Connection.objects.create(student=student, tutor=tutor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("tutor/connection-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "Peninsula Bridge: Tutoring Connection Established | Conexión de Tutoría!",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection,

            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()


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

        global connection

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
            email_list.append(student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("tutor/connection-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "Peninsula Bridge: Tutoring Connection Established | Conexión de Tutoría!",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()

        else:
            rel = Connection.objects.create(student=student, tutor=tutor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(tutor.email)
            email_list.append(student.parent1_email)
            email_list.append(student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            html_content = render_to_string("tutor/connection-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                "Peninsula Bridge: Tutoring Connection Established | Conexión de Tutoría!",
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection

            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ConnectionListView(ListView):
    model = Connection
    template_name = 'tutor/connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all().order_by('-created')
        return qs




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ConnectionDetailView(DetailView):
    model = Connection
    template_name = 'tutor/connection-detail.html'

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

        # email_list = []
        # email_list.append(student.email)
        # email_list.append(tutor.email)
        # email_list.append(student.parent1_email)
        # email_list.append(student.academic_advisor_email)

        # program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))

        # email_list.extend(program_manager_email_list)

        # html_content = render_to_string("tutor/disconnection-email.html", {'student': student, 'tutor': tutor })
        # text_context = strip_tags(html_content)
        # email = EmailMultiAlternatives(
        #     "Peninsula Bridge: Tutoring Disconnection",
        #     text_context,
        #     'Tutoring Program - Peninsula Bridge',
        #     email_list,
        # )

        # email.attach_alternative(html_content, "text/html")
        # email.send()
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class SessionListView(ListView):
    model = Session
    template_name = 'tutor/session-list.html'

    def get_queryset(self):
        qs = Session.objects.filter(submit_status=True).order_by('-created')
        return qs




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class SessionDetailView(DetailView):
    model = Session
    template_name = 'tutor/session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def generate_session_form(request):
    
    active_connection = Connection.objects.exclude(status='disconnected')

    global connection

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("https://www.admin.peninsulabridge.org/tutoring/" + session_generated_pk + "/submit-feedback/")

        tutor = x.tutor
        email = x.tutor.email

        form_link = "https://www.admin.peninsulabridge.org/tutoring/" + session_generated_pk + "/submit-feedback/"

        html_content = render_to_string("tutor/weekly-feedback-email.html", {'tutor': tutor, 'form_link': form_link })
        text_context = strip_tags(html_content)

        connection.open()

        email = EmailMultiAlternatives(
            "Peninsula Bridge Tutoring: Required Weekly Feedback Form",
            text_context,
            'Tutoring Program - Peninsula Bridge',
            [email],
            connection=connection
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
        connection.close()
        time.sleep(5)


    context = {'z':z}

    return render(request, 'tutor/session-form-link.html', context)

    


class SessionUpdateView(UpdateView):
    form_class = SessionModelForm
    model = Session
    template_name = 'tutor/submit-session-feedback.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session

    def form_valid(self, form):
        self.object.submit_status = True
        self.object = form.save()
        return redirect('profiles:session-submitted')




def session_submitted(request):

    return render(request, 'tutor/session-submitted.html')



	
def tutor_profile_form(request):

    form = TutorModelForm()

    if request.method == 'POST':
        form = TutorModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'tutor'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Thank you for your interest in becoming a tutor! We will contact you through email once you have been connected with a student. In the meantime, feel free to reach out to us at tutoring@peninsulabridge.org with any questions.')
  
    context = {'form':form}

    return render(request, 'tutor/tutor-profile-form.html', context)


	
def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.role = 'student'
            new_role.save()
            form.save_m2m()
            return HttpResponse('Thank you for your interest in tutoring! We will contact you through email once you have been connected with a student. In the meantime, feel free to reach out to us at tutoring@peninsulabridge.org with any questions.')
  
    context = {'form':form}

    return render(request, 'tutor/student-profile-form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def dashboard(request):

    todays_date = timezone.now()
    thirty_days_ago = todays_date-timedelta(days=30)
    thirty_days_session = Session.objects.filter(submit_status=True).filter(updated__gte=thirty_days_ago, updated__lte=todays_date)


    # First Row
    num_session = thirty_days_session.count()
    hour_session = thirty_days_session.aggregate(Sum('length'))

    x = 0
    for tutor in Profile.objects.filter(role='tutor'):
        if tutor.get_friends_no() == 0:
            x = x + 1

    y = 0
    for student in Profile.objects.filter(role='student'):
        if student.get_friends_no() == 0:
            y = y + 1

    # Second Row
    num_tutor = Profile.objects.filter(role='tutor').count()
    inactive_conn = Connection.objects.filter(status='inactive').count()
    connected_conn = Connection.objects.filter(status='connected').count()
    thirty_days_discon_connection = Connection.objects.filter(status='disconnected').filter(updated__gte=thirty_days_ago, updated__lte=todays_date).count()

    unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()

    # Third Row

    z = []
    for session in thirty_days_session:
        z.append(list(session.get_subjects().values('name')))   

    flat_list = [item for sublist in z for item in sublist]

    unique_counts = dict(collections.Counter(e['name'] for e in flat_list))

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
    
    
    # Fourth Row  

    tutor_list = []
    for session in Session.objects.filter(submit_status=True):
        tutor_list.append(session.connection.tutor.first_name) 

    hour_list = []
    for session in Session.objects.filter(submit_status=True):
        hour_list.append(session.length) 

    my_dict = defaultdict(list)
    for k, v in zip(tutor_list, hour_list):
        my_dict[k].append(v)

    top_tutor = {k: sum(filter(None, v)) for (k, v) in my_dict.items()}
    top_tutor = dict(sorted(top_tutor.items(), key=lambda item: item[1], reverse=False))
    top_tutor = list(top_tutor.items())[:25]
    top_tutor = dict(top_tutor)


    tutor_month = Profile.objects.filter(role='tutor').annotate(month=TruncMonth('created')).values('month').annotate(total=Count('first_name'))
    student_month = Profile.objects.filter(role='student').annotate(month=TruncMonth('created')).values('month').annotate(total=Count('first_name'))
    tutor_student_month = Profile.objects.all().annotate(month=TruncMonth('created')).values('month').annotate(total=Count('first_name'))


    # Fifth Row  

    avg_eng_prod_month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(rate=Avg('rate')).annotate(prod=Avg('productivity'))
    this_year = datetime.now().year

    #ELA
    ela = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='English Language Arts (ELA)').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    ela_list = []
    for l in ela:
        for c, m in l.items():
            ela_list.append(m)

    ela_dict = dict(zip(ela_list[::2], ela_list[1::2]))

    ela_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in ela_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            ela_dict.setdefault(mmyyyy, 0)

    ela_dict = dict(sorted(ela_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    ela_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in ela_dict.items()}

    #Science
    science = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='Science').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    sc_list = []
    for l in science:
        for c, m in l.items():
            sc_list.append(m)

    sc_dict = dict(zip(sc_list[::2], sc_list[1::2]))

    sc_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in sc_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            sc_dict.setdefault(mmyyyy, 0)

    sc_dict = dict(sorted(sc_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    sc_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in sc_dict.items()}

    #Math
    math = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='Math').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    math_list = []
    for l in math:
        for c, m in l.items():
            math_list.append(m)

    math_dict = dict(zip(math_list[::2], math_list[1::2]))

    math_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in math_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            math_dict.setdefault(mmyyyy, 0)

    math_dict = dict(sorted(math_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    math_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in math_dict.items()}



    #Homework Completion
    hc = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='Homework Completion').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    hc_list = []
    for l in hc:
        for c, m in l.items():
            hc_list.append(m)

    hc_dict = dict(zip(hc_list[::2], hc_list[1::2]))

    hc_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in hc_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            hc_dict.setdefault(mmyyyy, 0)

    hc_dict = dict(sorted(hc_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    hc_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in hc_dict.items()}


    #History/Social Studies
    his = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='History/Social Studies').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    his_list = []
    for l in his:
        for c, m in l.items():
            his_list.append(m)

    his_dict = dict(zip(his_list[::2], his_list[1::2]))

    his_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in his_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            his_dict.setdefault(mmyyyy, 0)

    his_dict = dict(sorted(his_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    his_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in his_dict.items()}


    #Writing
    wr = Subjectcalculation.objects.filter(updated__year=this_year).filter(name='Writing').annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('id'))

    wr_list = []
    for l in wr:
        for c, m in l.items():
            wr_list.append(m)

    wr_dict = dict(zip(wr_list[::2], wr_list[1::2]))

    wr_dict = {datetime.strptime(str(key), '%Y-%m-%d').strftime('%m-%Y'): val for key, val in wr_dict.items()}

    for year1 in range(this_year, this_year + 1):
        for month1 in range(1, 13):
            mmyyyy = '{:02}-{:04}'.format(month1, year1)
            wr_dict.setdefault(mmyyyy, 0)

    wr_dict = dict(sorted(wr_dict.items(), key = lambda x:datetime.strptime(x[0], '%m-%Y'), reverse=False))
    wr_dict = {datetime.strptime(str(key), '%m-%Y').strftime('%b-%Y'): val for key, val in wr_dict.items()}

    # Sixth Row  

    recent_session = Session.objects.filter(submit_status=True).order_by('-updated')[:5]


    context = {'month':month,
                'x':x,
                'y':y,
                'num_session':num_session,
                'hour_session':hour_session,
                'recent_session':recent_session,
                'unique_counts':unique_counts,
                'num_tutor': num_tutor,
                'inactive_conn': inactive_conn,
                'connected_conn': connected_conn,
                'thirty_days_discon_connection': thirty_days_discon_connection,
                'top_tutor': top_tutor,
                'tutor_month': tutor_month,
                'student_month': student_month,
                'tutor_student_month': tutor_student_month,
                'avg_eng_prod_month': avg_eng_prod_month,
                'ela_dict': ela_dict,
                'sc_dict': sc_dict,
                'math_dict': math_dict,
                'hc_dict': hc_dict,
                'his_dict': his_dict,
                'wr_dict': wr_dict,
                'unanswered_question_num': unanswered_question_num,

                }

    return render(request, 'tutor/dashboard.html', context)




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

    return render(request, 'tutor/connection-list-search.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def check_connection_status(request):

    todays_date = timezone.now()
    three_weeks_ago = todays_date-timedelta(days=21)

    active_connection = Connection.objects.filter(status='connected')

    inactive_list = [0, 0, 0]

    inactive_submit_status_list = [False, False, False]

    global connection

    for x in active_connection:

        list_status = []
        for z in x.get_all_sessions_three_all():
            list_status.append(z.submit_status)


        if list_status == inactive_submit_status_list:

            x.status = 'inactive'
            x.flag = True
            x.save()
            email_list = []
            email_list.append(x.student.parent1_email)
            email_list.append(x.student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)
            student = x.student
            tutor = x.tutor
            subject = "Inactive Tutoring Connection " + "| " + student.first_name + " and " + tutor.first_name

            html_content = render_to_string("tutor/connection-inactive-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()

            email = EmailMultiAlternatives(
                subject,
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()


        list_meet = []
        for y in x.get_all_sessions_three():
            list_meet.append(y.meet)

        if list_meet == inactive_list:
            x.status = 'inactive'
            x.flag = True
            x.save()
            email_list = []
            email_list.append(x.student.parent1_email)
            email_list.append(x.student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='tutor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            student = x.student
            tutor = x.tutor
            subject = "Inactive Tutoring Connection " + "| " + student.first_name + " and " + tutor.first_name

            html_content = render_to_string("tutor/connection-inactive-email.html", {'student': student, 'tutor': tutor })
            text_context = strip_tags(html_content)

            connection.open()
            email = EmailMultiAlternatives(
                subject,
                text_context,
                'Tutoring Program - Peninsula Bridge',
                email_list,
                connection=connection
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            connection.close()

    return HttpResponse("Connection Status Checked")



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'tutor/question-list.html'

    def get_queryset(self):
        qs = Question.objects.all().order_by('status').reverse()
        return qs



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
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
    return redirect('profiles:dashboard')



# def export_question(request):

#     questions = Question.objects.all()
#     response = HttpResponse('')
#     response['Content-Disposition'] = 'attachment; filename=questions.csv'
#     writer = csv.writer(response)
#     writer.writerow(['id', 'tutor', 'question', 'action', 'status', 'updated', 'created'])
#     questions = questions.values_list('id', 'tutor__first_name', 'question', 'action', 'status', 'updated', 'created')
#     for q in questions:
#         writer.writerow(q)
#     return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])
def export_tutoring_tutor_list(request):

    tutors = Profile.objects.filter(role='tutor')
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=tutoring_tutor_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'phone', 'grade', 'avatar', 'email', 'subjects', 'languages', 'school', 'student_capacity', 'question', 'age', 'student', 'date_added', 'flag'])
    
    for q in tutors:
        writer.writerow([q.id, q.first_name, q.last_name, q.phone, q.grade, q.avatar, q.email, '|'.join(c.name for c in q.subjects.all()), '|'.join(c.name for c in q.languages.all()), q.school, q.student_capacity, q.question, q.age, '|'.join(c.first_name + ' ' + c.last_name for c in q.friends.all()), q.created, q.flag])
    return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])
def export_tutoring_student_list(request):

    students = Profile.objects.filter(role='student')
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=tutoring_student_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'student_grade', 'academic_advisor', 'email', 'subjects', 'school', 'parent1_first_name', 'parent1_last_name', 'parent1_phone',
         'parent1_email', 'parent_languages', 'comfortable_share_phone', 'permission_share_grade', 'optional_school_loop_profile_link', 'optional_school_loop_username', 'optional_school_loop_password',
         'tutor', 'date_added', 'flag'])
    
    for q in students:
        writer.writerow([q.id, q.first_name, q.last_name, q.student_grade, q.academic_advisor, q.email, 
        '|'.join(c.name for c in q.subjects.all()), q.school, q.parent1_first_name, q.parent1_last_name, q.parent1_phone, q.parent1_email,
        '|'.join(c.name for c in q.parent_languages.all()), q.comfortable_share_phone, q.permission_share_grade, q.optional_school_loop_profile_link, q.optional_school_loop_username,
        q.optional_school_loop_password, '|'.join(c.first_name + ' ' + c.last_name for c in q.friends.all()), q.created, q.flag ])
        
    return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])
def export_tutoring_connection_list(request):

    connections = Connection.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=tutoring_connection_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'created', 'student', 'tutor', 'status', 'updated', 'flag'])
    
    for q in connections:
        writer.writerow([q.id, q.created, q.student.first_name + ' ' + q.student.last_name,
        q.tutor.first_name + ' ' + q.tutor.last_name, q.status, q.updated, q.flag])
        
    return response



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])
def export_tutoring_session_list(request):

    sessions = Session.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=tutoring_session_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'connection', 'meet', 'length', 'subjects', 'updated', 'created', 'help', 'support', 'othersupport', 'rate',
    'productivity', 'question', 'disconnect', 'submit_status', 'flag', 'reason_disconnect'])
    
    for q in sessions:
        writer.writerow([q.id, q.connection, q.meet, q.length, '|'.join(c.name for c in q.subjects.all()), q.updated,
        q.created, q.help, '|'.join(c.name for c in q.support.all()), q.othersupport, q.rate, q.productivity,
        q.question, q.disconnect, q.submit_status, q.flag, q.reason_disconnect])
        
    return response



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ProfileNoteUpdateView(UpdateView):
    form_class = ProfileNoteModelForm
    model = Profile
    template_name = 'tutor/note-update.html'

    def get_success_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.object.slug})



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class ConnectionNoteUpdateView(UpdateView):
    form_class = ConnectionNoteModelForm
    model = Connection
    template_name = 'tutor/note-update.html'

    def get_success_url(self):
        return reverse("profiles:connection-detail-view", kwargs={"pk": self.object.pk})




@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def search_question(request):
    if request.method == 'POST':
        source = request.POST.get('status')
        qs = Question.objects.all().order_by('-created').filter(source=source)

    context = {'qs':qs}

    return render(request, 'tutor/question-list-search.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])	
def change_status_tutor(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_id')
        tutor_obj = Profile.objects.get(id=tutor_id)

        if tutor_obj.status == 'active':
            Profile.objects.filter(id=tutor_id).update(status='deactivated')

        else:
            Profile.objects.filter(id=tutor_id).update(status='active')

        status = Profile.objects.filter(id=tutor_id).values('status')
        status = status[0]['status']

        data = {
            'status': status,
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class TutorProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'tutor/tutor-confirm-delete.html'
    success_url = reverse_lazy('profiles:tutor-profiles-view')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        obj = Profile.objects.get(id=id)
        return obj





@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['tutor', 'admin']), name='dispatch')
class StudentProfileDeleteView(DeleteView):
    model = Profile
    template_name = 'tutor/student-confirm-delete.html'
    success_url = reverse_lazy('profiles:student-profiles-view')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        obj = Profile.objects.get(id=id)
        return obj



@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor', 'admin'])
def feedback_form_status(request):

    active_connection = Connection.objects.exclude(status='disconnected')

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

    return render(request, 'tutor/feedback-form-status.html', context)