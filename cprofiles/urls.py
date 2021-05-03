from django.urls import path
from .views import (
    home_view,
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

   
)


app_name = 'cprofiles'

urlpatterns = [
    path('cprofiles/', home_view, name='cprofiles'),
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


    
]