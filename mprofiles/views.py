from django.shortcuts import render
from .models import Mentor, Student, Connection, Session
from django.views.generic import ListView, DetailView, UpdateView
from core.decorators import unauthenticated_user, allowed_users
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from .forms import MentorModelForm, StudentModelForm, SessionModelForm
from django.urls import reverse_lazy, reverse
from django.db.models.functions import TruncMonth
import collections
from django.db.models import Sum, Avg
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User




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
        students = Student.objects.all()
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
        mentors = Mentor.objects.all()
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

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

            send_mail('Connection Established',
            content,
            'Mentor Program',
            email_list,
            fail_silently=False
            )
    

        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

            send_mail('Connection Established',
            content,
            'Mentor Program',
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

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

            send_mail('Connection Established',
            content,
            'Mentor Program',
            email_list,
            fail_silently=False
            )
            
        else:
            rel = Connection.objects.create(student=student, mentor=mentor, status='connected')

            email_list = []
            email_list.append(student.email)
            email_list.append(mentor.email)
            email_list.append(student.academic_advisor_email)

            content = "Connection is established between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

            send_mail('Connection Established',
            content,
            'Mentor Program',
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

        email_list = []
        email_list.append(student.email)
        email_list.append(mentor.email)
        email_list.append(student.academic_advisor_email)

        program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))

        email_list.extend(program_manager_email_list)

        content = "Connection is disconnected between Student " + student.first_name + " " + student.last_name + " " + "Mentor" + " " + mentor.first_name + " " + mentor.last_name

        send_mail('Connection Disconnected',
        content,
        'Mentor Program',
        email_list,
        fail_silently=False
        )
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('mprofiles:mentor-profiles-list')



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def mentor_profile_form(request):

    form = MentorModelForm()

    if request.method == 'POST':
        form = MentorModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Mentor Profile Added')
  
    context = {'form':form}

    return render(request, 'mentor/mentor-profile-form.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def student_profile_form(request):

    form = StudentModelForm()

    if request.method == 'POST':
        form = StudentModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return HttpResponse('Student Profile Added')
  
    context = {'form':form}

    return render(request, 'mentor/student-profile-form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def generate_session_form(request):
    
    active_connection = Connection.objects.filter(status='connected')

    z = []
    for x in active_connection:
        session_generated = Session.objects.create(connection=x)
        session_generated_pk = str(session_generated.pk)
        z.append("http://127.0.0.1:8000/mprofiles/" + session_generated_pk + "/submit-feedback/")

        email = x.mentor.email

        content = "http://127.0.0.1:8000/mprofiles/" + session_generated_pk + "/submit-feedback/"

        send_mail('Please fill in the Session Feedback Form',
        content,
        'Mentor Program',
        [email],
        fail_silently=False
        )

    context = {'z':z}

    return render(request, 'mentor/session-form-link.html', context)




@method_decorator(login_required, name='dispatch')
@method_decorator(allowed_users(allowed_roles=['mentor', 'admin']), name='dispatch')
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
        return super().form_valid(form)





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
class StudentUpdateView(UpdateView):
    form_class = StudentModelForm
    model = Student
    template_name = 'update.html'

    def get_success_url(self):
        return reverse("mprofiles:student-profiles-detail", kwargs={"slug": self.object.slug})





@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor', 'admin'])
def dashboard(request):

    x = 0
    for mentor in Mentor.objects.all():
        if mentor.get_friends_no() == 0:
            x = x + 1

    y = 0
    for student in Student.objects.all():
        if student.get_friends_no() == 0:
            y = y + 1

    todays_date = timezone.now()
    thirty_days_ago = todays_date-timedelta(days=30)
    thirty_days_session = Session.objects.filter(submit_status=True).filter(created__gte=thirty_days_ago, created__lte=todays_date)

    num_session = thirty_days_session.count()
    hour_session = thirty_days_session.aggregate(Sum('length'))

    month = Session.objects.filter(submit_status=True).annotate(month=TruncMonth('updated')).values('month').annotate(total=Count('connection'))
    recent_session = Session.objects.filter(submit_status=True).order_by('-created')[:5]

    num_tutor = Mentor.objects.all().count()

    avg_rate = Session.objects.filter(submit_status=True).aggregate(Avg('rate'))

    inactive_conn = Connection.objects.filter(status='inactive').count()

    connected_conn = Connection.objects.filter(status='connected').count()

    context = {'month':month,
                'x':x,
                'y':y,
                'num_session':num_session,
                'hour_session':hour_session,
                'recent_session':recent_session,
                'num_tutor': num_tutor,
                'avg_rate': avg_rate,
                'inactive_conn': inactive_conn,
                'connected_conn': connected_conn,
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
                email_list.append(x.student.academic_advisor_email)
                program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
                email_list.extend(program_manager_email_list)

                content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.mentor.first_name + " " + x.mentor.last_name + " " + "because no session feedback form was submitted for two months straight"

                send_mail('Connection Inactive',
                content,
                'Mentor Program',
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
            email_list.append(x.student.academic_advisor_email)
            program_manager_email_list = list(i for i in User.objects.filter(groups__name='mentor').values_list('email', flat=True))
            email_list.extend(program_manager_email_list)

            content = "Connection is Inactive between Student " + x.student.first_name + " " + x.student.last_name + " " + "Tutor" + " " + x.mentor.first_name + " " + x.mentor.last_name + " " + "because 'Zero' Meets were submitted in Session Feedback form for two sessions straight."

            send_mail('Connection Inactive',
            content,
            'Mentor Program',
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