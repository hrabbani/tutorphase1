from django.urls import path
from .views import (
    MentorProfileListView,
    StudentProfileListView,
    MentorDetailView,
    StudentDetailView,
    MentorProfileDetailView,
    StudentProfileDetailView,
    flag_unflag_student,
    mentor_connect,
    student_connect,
    ConnectionListView,
    flag_unflag_connection,
    ConnectionDetailView,
    remove_connection,
    mentor_profile_form,
    student_profile_form,
    generate_session_form,
    SessionUpdateView,
    SessionListView,
    SessionDetailView,
    MentorUpdateView,
    StudentUpdateView,
    dashboard,
    check_connection_status,
    flag_unflag_mentor,
    flag_unflag_student,
    flag_unflag_session,
    QuestionListView,
    action_question,
    MentorNoteUpdateView,
    StudentNoteUpdateView,
    ConnectionNoteUpdateView,
    search_connection,
    export_mentoring_mentor_list,
    export_mentoring_student_list,
    export_mentoring_connection_list,
    export_mentoring_session_list,
    search_question,
   
)


app_name = 'mprofiles'

urlpatterns = [
    path('mentors/', MentorProfileListView.as_view(), name='mentor-profiles-list'),
    path('students/', StudentProfileListView.as_view(), name='student-profiles-list'),
    path('<slug>/mentor-profile-detail', MentorDetailView.as_view(), name='mentor-profiles-detail'),
    path('<slug>/student-profile-detail', StudentDetailView.as_view(), name='student-profiles-detail'),
    path('<slug>/mentor/connect/', MentorProfileDetailView.as_view(), name='mentor-connect-detail'),
    path('<slug>/student/connect/', StudentProfileDetailView.as_view(), name='student-connect-detail'),
    path('mentor-connect/', mentor_connect, name='mentor-connect'),
    path('student-connect/', student_connect, name='student-connect'),
    path('connections/', ConnectionListView.as_view(), name='connection-list'),
    path('flag-connection/', flag_unflag_connection, name='flag-connection'),
    path('<pk>/connection-detail', ConnectionDetailView.as_view(), name='connection-profile-detail'),
    path('remove-connect/', remove_connection, name='remove-connect'),
    path('mentor-profile-input/', mentor_profile_form, name='mentor-profile-form'),
    path('student-profile-input/', student_profile_form, name='student-profile-form'),
    path('generate-session-form/', generate_session_form, name='generate-session-form'),
    path('<pk>/submit-feedback/', SessionUpdateView.as_view(), name='submit-feedback'),
    path('sessions/', SessionListView.as_view(), name='session-list'),
    path('<pk>/session/', SessionDetailView.as_view(), name='session-detail'),
    path('<slug>/mentor-update-profile', MentorUpdateView.as_view(), name='mentor-update-profile'),
    path('<slug>/student-update-profile', StudentUpdateView.as_view(), name='student-update-profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('check-connection-status/', check_connection_status, name='check-connection-status'),
    path('flag-mentor', flag_unflag_mentor, name='flag-mentor'),
    path('flag-student', flag_unflag_student, name='flag-student'),
    path('flag-session', flag_unflag_session, name='flag-session'),
    path('questions/', QuestionListView.as_view(), name='question-list-view'),
    path('action-question/', action_question, name='action-question'),
    path('<slug>/mentor-note-update-profile', MentorNoteUpdateView.as_view(), name='mentor-note-update-profile'),
    path('<slug>/student-note-update-profile', StudentNoteUpdateView.as_view(), name='student-note-update-profile'),
    path('<pk>/connection-note-update-profile', ConnectionNoteUpdateView.as_view(), name='connection-note-update-profile'),
    path('search-connection/', search_connection, name='search-connection'),
    path('export-mentoring-mentor-list/', export_mentoring_mentor_list, name='export-mentoring-mentor-list'),
    path('export-mentoring-student-list/', export_mentoring_student_list, name='export-mentoring-student-list'),
    path('export-mentoring-connection-list/', export_mentoring_connection_list, name='export-mentoring-connection-list'),
    path('export-mentoring-ession-list/', export_mentoring_session_list, name='export-mentoring-session-list'),
    path('search-question/', search_question, name='search-question'),


    
]