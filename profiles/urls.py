from django.urls import path
from .views import ( 
    connect,
    TutorProfileListView,
    TutorProfileDetailView,
    StudentProfileListView,
    StudentProfileDetailView,
    ConnectionListView,
    remove_connection,
    SessionListView,
    ProfileDetailView,
    SessionDetailView,
    tutor_profile_form,
    student_profile_form,
    dashboard,
    
    

)

app_name = 'profiles'

urlpatterns = [
    path('tutors/', TutorProfileListView.as_view(), name='tutor-profiles-view'),
    path('students/', StudentProfileListView.as_view(), name='student-profiles-view'),
    path('send-connect/', connect, name='connect'),
    path('<slug>/connect/tutor/', TutorProfileDetailView.as_view(), name='tutor-detail-view'),
    path('<slug>/connect/student/', StudentProfileDetailView.as_view(), name='student-detail-view'),
    path('connections/', ConnectionListView.as_view(), name='connection-view'),
    path('remove-connect/', remove_connection, name='remove-connect'),
    path('sessions/', SessionListView.as_view(), name='session-view'),
    path('<slug>/profile-detail', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('<pk>/session/', SessionDetailView.as_view(), name='session-detail-view'),
    path('tutor-profile-input/', tutor_profile_form, name='tutor-profile-form'),
    path('student-profile-input/', student_profile_form, name='student-profile-form'),
    path('dashboard/', dashboard, name='dashboard'),


    
]