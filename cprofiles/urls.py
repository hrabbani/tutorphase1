from django.urls import path
from .views import (
    MentorUpdateView,
    MentorProfileListView,
    StudentProfileListView,
    MentorDetailView,
    StudentDetailView,
    MentorProfileDetailView,
    StudentProfileDetailView,
    mentor_connect,
    student_connect,
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
    StudentUpdateView,
    check_connection_status,
    flag_unflag_connection,
    flag_unflag_student,
    flag_unflag_mentor,
    flag_unflag_session,
    QuestionListView,
    action_question,
    ParentSessionListView,
    flag_unflag_parent_session,
    ParentSessionDetailView,
    ParentSessionUpdateView,
    search_connection,
    export_choice_mentor_list,
    export_choice_student_list,
    export_choice_connection_list,
    export_choice_session_list,
    ParentSessionSpanishUpdateView,
    StudentNoteUpdateView,
    ConnectionNoteUpdateView,
    feedback_form_status,
    change_status_mentor,
    change_status_student,
    MentorProfileDeleteView,
    StudentProfileDeleteView,
    generate_session_form_parent,
   
)


app_name = 'cprofiles'

urlpatterns = [
    path('mentors/', MentorProfileListView.as_view(), name='mentor-profiles-list'),
    path('students/', StudentProfileListView.as_view(), name='student-profiles-list'),
    path('<slug>/mentor-profile-detail', MentorDetailView.as_view(), name='mentor-profiles-detail'),
    path('<slug>/student-profile-detail', StudentDetailView.as_view(), name='student-profiles-detail'),
    path('mentor-connect/', mentor_connect, name='mentor-connect'),
    path('student-connect/', student_connect, name='student-connect'),
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
    path('check-connection-status/', check_connection_status, name='check-connection-status'),
    path('flag-connection/', flag_unflag_connection, name='flag-connection'),
    path('flag-student/', flag_unflag_student, name='flag-student'),
    path('flag-mentor/', flag_unflag_mentor, name='flag-mentor'),
    path('flag-session/', flag_unflag_session, name='flag-session'),
    path('questions/', QuestionListView.as_view(), name='question-list-view'),
    path('action-question/', action_question, name='action-question'),
    path('parent-sessions/', ParentSessionListView.as_view(), name='parent-session-list'),
    path('flag-parent-session/', flag_unflag_parent_session, name='flag-parent-session'),
    path('<pk>/parent-session/', ParentSessionDetailView.as_view(), name='parent-session-detail'),
    path('<pk>/submit-parent-feedback/', ParentSessionUpdateView.as_view(), name='submit-parent-feedback'),
    path('search-connection/', search_connection, name='search-connection'),
    path('export-choice-mentor-list/', export_choice_mentor_list, name='export-choice-mentor-list'),
    path('export-choice-student-list/', export_choice_student_list, name='export-choice-student-list'),
    path('export-choice-connection-list/', export_choice_connection_list, name='export-choice-connection-list'),
    path('export-choice-session-list/', export_choice_session_list, name='export-choice-session-list'),
    path('<pk>/submit-parent-feedback-spanish/', ParentSessionSpanishUpdateView.as_view(), name='submit-parent-feedback-spanish'),
    path('<slug>/student-note-update-profile', StudentNoteUpdateView.as_view(), name='student-note-update-profile'),
    path('<pk>/connection-note-update-profile', ConnectionNoteUpdateView.as_view(), name='connection-note-update-profile'),
    path('feedback-form-status/', feedback_form_status, name='feedback-form-status'),
    path('change-status-mentor/', change_status_mentor, name='change-status-mentor'),
    path('change-status-student/', change_status_student, name='change-status-student'),
    path('<pk>/mentor-delete/', MentorProfileDeleteView.as_view(), name='mentor-profile-delete'),
    path('<pk>/student-delete/', StudentProfileDeleteView.as_view(), name='student-profile-delete'),
    path('generate-session-form-parent/', generate_session_form_parent, name='generate-session-form-parent'),

    
]