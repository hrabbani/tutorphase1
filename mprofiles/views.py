from django.shortcuts import render
from .models import Mentor, Student, Connection, Session, Question
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from core.decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from .forms import MentorModelForm, StudentModelForm, SessionModelForm, MentorNoteModelForm, StudentNoteModelForm, ConnectionNoteModelForm
from django.urls import reverse_lazy, reverse
from django.db.models.functions import TruncMonth
import collections
from django.db.models import Sum, Avg
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from collections import defaultdict
import csv
import time




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorProfileListView(ListView):
    model = Mentor
    template_name = 'mentor/mentor-profile-list.html'

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
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentProfileListView(ListView):
    model = Student
    template_name = 'mentor/student-profile-list.html'

    def get_queryset(self):
        qs = Student.objects.all()
        return qs



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorDetailView(DetailView):
    model = Mentor
    template_name = 'mentor/mentor-detail.html'

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
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = 'mentor/student-detail.html'

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
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorProfileDetailView(DetailView):
    model = Mentor
    template_name = 'mentor/mentor-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        mentor = Mentor.objects.get(slug=slug)
        return mentor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.filter(status='active')
        students_ = []
        for item in students:
            students_.append(item)
        context["students"] = students_
        return context



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentProfileDetailView(DetailView):
    model = Student
    template_name = 'mentor/student-connect.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        student = Student.objects.get(slug=slug)
        return student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mentors = Mentor.objects.filter(status='active')
        mentors_ = []
        for item in mentors:
            mentors_.append(item)
        context["mentors"] = mentors_
        return context





@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
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
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Dear " + student.first_name + " " + student.last_name + " and " + mentor.first_name + " " + mentor.last_name + ", \n\nWelcome to Peninsula Bridge's High School Mentor Program! We are so excited to introduce you two to each other. \n\n" + mentor.first_name + ", we ask that you please reach out to " + student.first_name + " within the next two weeks to schedule your first meeting. And " + student.first_name + ", we ask that you please make sure to respond immediately. Here is a suggested agenda to follow for your first meeting: https://docs.google.com/document/d/1IeSDmICouu2yAjdWgW3urVS99de35z7Sa6OfByIkXT8/edit. Please let me know when you plan to meet and I will attend as well if I can. " + student.first_name + ", please find a time when at least one parent/guardian can attend with you for the first few minutes to exchange contact information. This is required only for the first meeting, all subsequent meetings should be only the mentor and the mentee. \n\nAs a reminder, the minimum requirement to meet with each other is at least once per month. It is important that you both be responsive to each other's communication throughout the year. And " + student.first_name + ", there is so much you can gain from this relationship (ex. networking opportunities, personal support, college and career advice, exposure to different ideas,etc), however, please note that will only happen if you show up to every meeting with eagerness, curiosity, and determination. Have fun! \n\nIf you have any questions or concerns, please reach out to me at komal@peninsulabridge.org. \n\nBest, \nKomal Goel"

            
            send_mail('Introducing you to your Peninsula Bridge Mentor/Mentee',
            content,
            'Mentor Program - Peninsula Bridge',
            email_list,
            fail_silently=False
            )
    

        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Dear " + student.first_name + " " + student.last_name + " and " + mentor.first_name + " " + mentor.last_name + ", \n\nWelcome to Peninsula Bridge's High School Mentor Program! We are so excited to introduce you two to each other. \n\n" + mentor.first_name + ", we ask that you please reach out to " + student.first_name + " within the next two weeks to schedule your first meeting. And " + student.first_name + ", we ask that you please make sure to respond immediately. Here is a suggested agenda to follow for your first meeting: https://docs.google.com/document/d/1IeSDmICouu2yAjdWgW3urVS99de35z7Sa6OfByIkXT8/edit. Please let me know when you plan to meet and I will attend as well if I can. " + student.first_name + ", please find a time when at least one parent/guardian can attend with you for the first few minutes to exchange contact information. This is required only for the first meeting, all subsequent meetings should be only the mentor and the mentee. \n\nAs a reminder, the minimum requirement to meet with each other is at least once per month. It is important that you both be responsive to each other's communication throughout the year. And " + student.first_name + ", there is so much you can gain from this relationship (ex. networking opportunities, personal support, college and career advice, exposure to different ideas,etc), however, please note that will only happen if you show up to every meeting with eagerness, curiosity, and determination. Have fun! \n\nIf you have any questions or concerns, please reach out to me at komal@peninsulabridge.org. \n\nBest, \nKomal Goel"

            send_mail('Introducing you to your Peninsula Bridge Mentor/Mentee',
            content,
            'Mentor Program - Peninsula Bridge',
            email_list,
            fail_silently=False
            )
 
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('mprofiles:mentor-profiles-list')




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
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
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Dear " + student.first_name + " " + student.last_name + " and " + mentor.first_name + " " + mentor.last_name + ", \n\nWelcome to Peninsula Bridge's High School Mentor Program! We are so excited to introduce you two to each other. \n\n" + mentor.first_name + ", we ask that you please reach out to " + student.first_name + " within the next two weeks to schedule your first meeting. And " + student.first_name + ", we ask that you please make sure to respond immediately. Here is a suggested agenda to follow for your first meeting: https://docs.google.com/document/d/1IeSDmICouu2yAjdWgW3urVS99de35z7Sa6OfByIkXT8/edit. Please let me know when you plan to meet and I will attend as well if I can. " + student.first_name + ", please find a time when at least one parent/guardian can attend with you for the first few minutes to exchange contact information. This is required only for the first meeting, all subsequent meetings should be only the mentor and the mentee. \n\nAs a reminder, the minimum requirement to meet with each other is at least once per month. It is important that you both be responsive to each other's communication throughout the year. And " + student.first_name + ", there is so much you can gain from this relationship (ex. networking opportunities, personal support, college and career advice, exposure to different ideas,etc), however, please note that will only happen if you show up to every meeting with eagerness, curiosity, and determination. Have fun! \n\nIf you have any questions or concerns, please reach out to me at komal@peninsulabridge.org. \n\nBest, \nKomal Goel"

            send_mail('Introducing you to your Peninsula Bridge Mentor/Mentee',
            content,
            'Mentor Program - Peninsula Bridge',
            email_list,
            fail_silently=False
            )
            
        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Dear " + student.first_name + " " + student.last_name + " and " + mentor.first_name + " " + mentor.last_name + ", \n\nWelcome to Peninsula Bridge's High School Mentor Program! We are so excited to introduce you two to each other. \n\n" + mentor.first_name + ", we ask that you please reach out to " + student.first_name + " within the next two weeks to schedule your first meeting. And " + student.first_name + ", we ask that you please make sure to respond immediately. Here is a suggested agenda to follow for your first meeting: https://docs.google.com/document/d/1IeSDmICouu2yAjdWgW3urVS99de35z7Sa6OfByIkXT8/edit. Please let me know when you plan to meet and I will attend as well if I can. " + student.first_name + ", please find a time when at least one parent/guardian can attend with you for the first few minutes to exchange contact information. This is required only for the first meeting, all subsequent meetings should be only the mentor and the mentee. \n\nAs a reminder, the minimum requirement to meet with each other is at least once per month. It is important that you both be responsive to each other's communication throughout the year. And " + student.first_name + ", there is so much you can gain from this relationship (ex. networking opportunities, personal support, college and career advice, exposure to different ideas,etc), however, please note that will only happen if you show up to every meeting with eagerness, curiosity, and determination. Have fun! \n\nIf you have any questions or concerns, please reach out to me at komal@peninsulabridge.org. \n\nBest, \nKomal Goel"

            send_mail('Introducing you to your Peninsula Bridge Mentor/Mentee',
            content,
            'Mentor Program - Peninsula Bridge',
            email_list,
            fail_silently=False
            )

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('mprofiles:mentor-profiles-list')



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class ConnectionListView(ListView):
    model = Connection
    template_name = 'mentor/connection-list.html'

    def get_queryset(self):
        qs = Connection.objects.all().order_by('-created')
        return qs


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
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



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class ConnectionDetailView(DetailView):
    model = Connection
    template_name = 'mentor/connection-detail.html'

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
@allowed_users(allowed_roles=['mentor', 'admin'])
def remove_connection(request):
    if request.method=='POST':
        student_pk = request.POST.get('student_pk')
        mentor_pk = request.POST.get('mentor_pk')
        student = Student.objects.get(pk=student_pk)
        mentor = Mentor.objects.get(pk=mentor_pk)

        rel = Connection.objects.get(Q(student=student), Q(mentor=mentor))
        rel.status = 'disconnected'
        rel.save()

        # email_list = []
        # email_list.append(student.email)
        # email_list.append(mentor.email)
        # email_list.append(student.academic_advisor_email)

        # program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))

        # email_list.extend(program_manager_email_list)

        # content = "Connection is disconnected between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

        # send_mail('Connection Disconnected',
        # content,
        # 'Mentor Program',
        # email_list,
        # fail_silently=False
        # )
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('mprofiles:mentor-profiles-list')




def mentor_profile_form(request):

    form = MentorModelForm()

    if request.method == 'POST':
        form = MentorModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for your interest in becoming a mentor.  Someone will be in touch shortly to schedule a short phone interview.  Also, there will be a virtual training workshop in mid-September (date TBD).')
  
    context = {'form':form}

    return render(request, 'mentor/mentor-profile-form.html', context)




def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for signing up for this year’s mentoring program! We will contact you over email once you have been paired with a mentor.')
  
    context = {'form':form}

    return render(request, 'mentor/student-profile-form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def generate_session_form(request):
    
    active_connection = Connection.objects.exclude(status='disconnected')

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("https://www.admin.peninsulabridge.org/mentoring/" + session_generated_pk + "/submit-feedback/")

        email = x.mentor.email
        name1 = x.mentor.first_name
        name2 = x.mentor.last_name

        student_first = x.student.first_name
        student_last = x.student.last_name


        content = "Dear " + name1 + " " + name2 + "," "\n\nThank you for volunteering your time to support " + student_first + "! Please take 3-5 minutes to complete the following feedback form: " + "https://www.admin.peninsulabridge.org/mentoring/" + session_generated_pk + "/submit-feedback/" + ". We will continue to send this form every month so we can support you with any concerns that arise in a faster and easier manner. \n\nThis is also a great place to reflect on your mentorship experience, tracking the progress your student is making and identifying the impact you are creating. Thank you for your support! \n\nIf you have any questions or concerns, please reach out to Komal at komal@peninsulabridge.org. \n\nYour Mentor Coordinator,\nKomal Goel"

        

        send_mail('Mentor Feedback Form - Peninsula Bridge',
        content,
        'Mentor Program - Peninsula Bridge',
        [email],
        fail_silently=False
        )
        
        time.sleep(5)


    context = {'z':z}

    return render(request, 'mentor/session-form-link.html', context)




class SessionUpdateView(UpdateView):
    form_class = SessionModelForm
    model = Session
    template_name = 'mentor/submit-session-feedback.html'
    success_url = reverse_lazy('profiles:session-submitted')

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session

    def form_valid(self, form):
        self.object.submit_status = True
        self.object = form.save()
        return redirect('profiles:session-submitted') 



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class SessionListView(ListView):
    model = Session
    template_name = 'mentor/session-list.html'

    def get_queryset(self):
        qs = Session.objects.filter(submit_status=True).order_by('-updated')
        return qs




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class SessionDetailView(DetailView):
    model = Session
    template_name = 'mentor/session-detail.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        session = Session.objects.get(pk=pk)
        return session



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorUpdateView(UpdateView):
    form_class = MentorModelForm
    model = Mentor
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("mprofiles:mentor-profiles-detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorNoteUpdateView(UpdateView):
    form_class = MentorNoteModelForm
    model = Mentor
    template_name = 'mentor/note-update.html'

    def get_success_url(self):
        return reverse("mprofiles:mentor-profiles-detail", kwargs={"slug": self.object.slug})




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentNoteUpdateView(UpdateView):
    form_class = StudentNoteModelForm
    model = Student
    template_name = 'mentor/note-update.html'

    def get_success_url(self):
        return reverse("mprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})


@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class ConnectionNoteUpdateView(UpdateView):
    form_class = ConnectionNoteModelForm
    model = Connection
    template_name = 'mentor/note-update.html'

    def get_success_url(self):
        return reverse("mprofiles:connection-profile-detail", kwargs={"pk": self.object.pk})



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentUpdateView(UpdateView):
    form_class = StudentModelForm
    model = Student
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("mprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})





@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def dashboard(request):

    # 1st Row

    todays_date = timezone.now()
    thirty_days_ago = todays_date-timedelta(days=30)
    thirty_days_session = Session.objects.filter(submit_status=True).filter(updated__gte=thirty_days_ago, updated__lte=todays_date)

    num_session = thirty_days_session.count()
    hour_session = thirty_days_session.aggregate(Sum('length'))

    x = 0
    for mentor in Mentor.objects.all():
        if mentor.get_friends_no() == 0:
            x = x + 1

    y = 0
    for student in Student.objects.all():
        if student.get_friends_no() == 0:
            y = y + 1

    avg_engagement = thirty_days_session.aggregate(Avg('rate'))


    # 2nd Row

    unanswered_question_num = Question.objects.filter(status="UNANSWERED").count()
    num_tutor = Mentor.objects.all().count()
    inactive_conn = Connection.objects.filter(status='inactive').count()
    connected_conn = Connection.objects.filter(status='connected').count()

    # 3rd Row

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
   
    avg_eng_meaning_month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(rate=Avg('rate'))
   

    # 4th Row

    recent_session = Session.objects.filter(submit_status=True).order_by('-created')[:5]



    context = {'month':month,
                'x':x,
                'y':y,
                'num_session':num_session,
                'hour_session':hour_session,
                'recent_session':recent_session,
                'num_tutor': num_tutor,
                'inactive_conn': inactive_conn,
                'connected_conn': connected_conn,
                'unanswered_question_num': unanswered_question_num,
                'avg_eng_meaning_month': avg_eng_meaning_month,
                'avg_engagement': avg_engagement,
                }

    return render(request, 'mentor/dashboard.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def check_connection_status(request):

    todays_date = timezone.now()
    eight_weeks_ago = todays_date-timedelta(days=60)

    active_connection = Connection.objects.filter(status='connected')

    inactive_list = [0, 0]

    for x in active_connection:
        for y in x.get_all_sessions():
            if y.updated >= eight_weeks_ago:
                break
            else:
                x.status = 'inactive'
                x.flag = True
                x.save()
                email_list = []
                program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
                email_list.extend(program_manager_email_list)

                content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.mentor.first_name + " " + x.mentor.last_name + " " + "because no session feedback form was submitted for two months straight"

                send_mail('Connection Inactive',
                content,
                'Mentor Program - Peninsula Bridge',
                email_list,
                fail_silently=False
                )

                break

        list_meet = []
        for y in x.get_all_sessions_two():
            list_meet.append(y.meet)

        if list_meet == inactive_list:
            x.status = 'inactive'
            x.flag = True
            x.save()
            email_list = []
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.mentor.first_name + " " + x.mentor.last_name + " " + "because 'Zero' Meets were submitted in Session Feedback form for two sessions straight."

            send_mail('Connection Inactive',
            content,
            'Mentor Program - Peninsula Bridge',
            email_list,
            fail_silently=False
            )

    return HttpResponse("Connection Status Checked")




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
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
@allowed_users(allowed_roles=['mentor', 'admin'])	
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
@allowed_users(allowed_roles=['mentor', 'admin'])	
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
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = 'mentor/question-list.html'

    def get_queryset(self):
        qs = Question.objects.all().order_by('status').reverse()
        return qs



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
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






@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def search_connection(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        qs = Connection.objects.all().order_by('-created').filter(status=status)

    context = {'qs':qs}

    return render(request, 'mentor/connection-list-search.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def export_mentoring_mentor_list(request):

    mentors = Mentor.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=mentoring_mentor_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'language', 'emergency_contact',
        'employment_status', 'employer_info', 'partner', 'hear', 'experience', 'reason', 'know', 'question1', 'answer1', 
        'question2', 'answer2', 'prefer_sex', 'geographical', 'commit', 'available', 'seminar', 'signature', 
        'grant', 'cont_student_bridge', 'check', 'spanish', 'question', 'student', 'date_added', 'flag'])
    
    for q in mentors:
        writer.writerow([q.id, q.first_name, q.last_name, q.avatar, q.email, q.phone, q.address, q.language, q.emergency_contact,
        q.employment_status, q.employer_info, q.partner, q.hear, q.experience, q.reason, q.know, q.question1, q.answer1, q.question2, q.answer2, q.prefer_sex, q.geographical,
        q.commit, q.available, q.seminar, q.signature, q.grant, q.cont_student_bridge, q.check, q.spanish, q.question,
        '|'.join(c.first_name + ' ' + c.last_name for c in q.friends.all()), q.created, q.flag])

    return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def export_mentoring_student_list(request):

    students = Student.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=mentoring_student_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'grade', 'school',
        'academic_advisor', 'academic_advisor_email', 'reason', 'know', 'question1', 'answer1', 'question2', 
        'answer2', 'prefer_sex', 'geographical', 'commit', 'available', 'seminar', 'signature',
        'mentor', 'date_added', 'flag'])
    
    for q in students:
        writer.writerow([q.id, q.first_name, q.last_name, q.avatar, q.email, q.phone, q.address, q.grade, q.school,
        q.academic_advisor, q.academic_advisor_email, q.reason, q.know, q.question1, q.answer1, q.question2,
        q.answer2, q.prefer_sex, q.geographical, q.commit, q.available, q.seminar, q.signature,
        '|'.join(c.first_name + ' ' + c.last_name for c in q.get_friends()), q.created, q.flag])

    return response





@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def export_mentoring_connection_list(request):

    connections = Connection.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=mentoring_connection_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'created', 'student', 'mentor', 'status', 'updated', 'flag', 'note'])
    
    for q in connections:
        writer.writerow([q.id, q.created, q.student.first_name + ' ' + q.student.last_name, q.mentor.first_name + ' ' + q.mentor.last_name, q.status, q.updated, q.flag, q.note])
        
    return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def export_mentoring_session_list(request):

    sessions = Session.objects.all()
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename=mentoring_session_list.csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'connection', 'meet', 'dialogue', 'length', 'summary', 'help', 'change', 'rate', 
    'meaningful', 'support', 'elaborate', 'urgent', 'question', 'updated', 'created', 'submit_status', 'flag'])
    
    for q in sessions:
        writer.writerow([q.id, q.connection, q.meet, q.dialogue, q.length, q.summary,
        q.help, q.change, q.rate, q.meaningful, '|'.join(c.name for c in q.support.all()), q.elaborate, 
        q.urgent, q.question, q.updated, q.created, q.submit_status, q.flag])
        
    return response





@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def search_question(request):
    if request.method == 'POST':
        source = request.POST.get('status')
        qs = Question.objects.all().order_by('-created').filter(source=source)

    context = {'qs':qs}

    return render(request, 'mentor/question-list-search.html', context)

 

 
@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def change_check_mentor(request):
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor_id')

        Mentor.objects.filter(id=mentor_id).update(check='yes')
       
        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



 
@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def change_uncheck_mentor(request):
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor_id')

        Mentor.objects.filter(id=mentor_id).update(check='no')
       
        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('profiles:dashboard')



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def change_status_mentor(request):
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor_id')
        mentor_obj = Mentor.objects.get(id=mentor_id)

        if mentor_obj.status == 'active':
            Mentor.objects.filter(id=mentor_id).update(status='deactivated')

        else:
            Mentor.objects.filter(id=mentor_id).update(status='active')

        status = Mentor.objects.filter(id=mentor_id).values('status')
        status = status[0]['status']

        data = {
            'status': status,
        }

        return JsonResponse(data, safe=False)
    return redirect('mprofiles:dashboard')



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def change_status_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student_obj = Student.objects.get(id=student_id)

        if student_obj.status == 'active':
            Student.objects.filter(id=student_id).update(status='deactivated')

        else:
            Student.objects.filter(id=student_id).update(status='active')

        status = Student.objects.filter(id=student_id).values('status')
        status = status[0]['status']

        data = {
            'status': status,
        }

        return JsonResponse(data, safe=False)
    return redirect('mprofiles:dashboard')




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class MentorProfileDeleteView(DeleteView):
    model = Mentor
    template_name = 'mentor/mentor-confirm-delete.html'
    success_url = reverse_lazy('mprofiles:mentor-profiles-list')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        obj = Mentor.objects.get(id=id)
        return obj



@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
class StudentProfileDeleteView(DeleteView):
    model = Student
    template_name = 'mentor/student-confirm-delete.html'
    success_url = reverse_lazy('mprofiles:student-profiles-list')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('pk')
        obj = Student.objects.get(id=id)
        return obj



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
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

    return render(request, 'mentor/feedback-form-status.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])	
def reactivate_connection(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')

        Connection.objects.filter(id=post_id).update(status='connected')        

        data = {
            # 'value': like.value,
            # 'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    return redirect('mprofiles:dashboard')