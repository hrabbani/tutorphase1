from django.urls import path
from .views import (
    MentorUpdateView,
    MentorProfileListView,
    StudentProfileListView,
    MentorDetailView,
    StudentDetailView,
    MentorProfileDetailView,
    StudentProfileDetailView,
    connect,
    ConnectionListView,
    remove_connection,
    TaskUpdateView,
    generate_session_form,
    update_session,
    SessionListView,
    ConnectionDetailView,
    SessionDetailView,
    mentor_profile_form,
    student_profile_form,
    dashboard,
    show_task_form,
    MentorUpdateView,
    StudentUpdateView

   
)


app_name = 'cprofiles'

urlpatterns = [
    path('mentors/', MentorProfileListView.as_view(), name='mentor-profiles-list'),
    path('students/', StudentProfileListView.as_view(), name='student-profiles-list'),
    path('<slug>/mentor-profile-detail', MentorDetailView.as_view(), name='mentor-profiles-detail'),
    path('<slug>/student-profile-detail', StudentDetailView.as_view(), name='student-profiles-detail'),
    path('send-connect/', connect, name='connect'),
    path('<slug>/connect/tutor/', MentorProfileDetailView.as_view(), name='mentor-connect-detail'),
    path('<slug>/connect/student/', StudentProfileDetailView.as_view(), name='student-connect-detail'),
    path('connections/', ConnectionListView.as_view(), name='connection-list'),
    path('remove-connect/', remove_connection, name='remove-connect'),
    path('<pk>/task-form/', TaskUpdateView.as_view(), name='task-form'),
    path('generate-session-form/', generate_session_form, name='generate-session-form'),
    path('<pk>/submit-feedback/', update_session, name="update_session"),
    path('sessions/', SessionListView.as_view(), name='session-list'),
    path('<pk>/connection-detail', ConnectionDetailView.as_view(), name='connection-profile-detail'),
    path('<pk>/session/', SessionDetailView.as_view(), name='session-detail'),
    path('remove-connect/', remove_connection, name='remove-connect'),
    path('mentor-profile-input/', mentor_profile_form, name='mentor-profile-form'),
    path('student-profile-input/', student_profile_form, name='student-profile-form'),
    path('dashboard/', dashboard, name='dashboard'),
    path('<pk>/show-task-form/', show_task_form, name='show-task-form'),
    path('<slug>/mentor-update-profile', MentorUpdateView.as_view(), name='mentor-update-profile'),
    path('<slug>/student-update-profile', StudentUpdateView.as_view(), name='student-update-profile'),




    
]