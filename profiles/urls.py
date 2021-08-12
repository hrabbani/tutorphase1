from django.urls import path
from .views import ( 
    flag_unflag_connection,
    tutor_connect,
    student_connect,
    TutorProfileListView,
    TutorProfileDetailView,
    StudentProfileListView,
    StudentProfileDetailView,
    ConnectionListView,
    remove_connection,
    SessionListView,
    ProfileDetailView,
    SessionDetailView,
    search_connection,
    tutor_profile_form,
    student_profile_form,
    dashboard,
    SessionUpdateView,
    generate_session_form,
    session_submitted,
    ConnectionDetailView,
    like_unlike_post,
    search_connection,
    check_connection_status,
    TutorUpdateView,
    StudentUpdateView,
    flag_unflag_connection,
    flag_unflag_tutor,
    flag_unflag_session,
    QuestionListView,
    action_question,
    export_tutoring_tutor_list,
    export_tutoring_student_list,
    export_tutoring_connection_list,
    export_tutoring_session_list,
    ProfileNoteUpdateView,
    ConnectionNoteUpdateView,
    search_question,
        

)

app_name = 'profiles'

urlpatterns = [
    path('tutors/', TutorProfileListView.as_view(), name='tutor-profiles-view'),
    path('students/', StudentProfileListView.as_view(), name='student-profiles-view'),
    path('tutor-connect/', tutor_connect, name='tutor-connect'),
    path('student-connect/', student_connect, name='student-connect'),
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
    path('<pk>/submit-feedback/', SessionUpdateView.as_view(), name='submit-feedback'),
    path('generate-session-form/', generate_session_form, name='generate-session-form'),
    path('session-submitted/', session_submitted, name='session-submitted'),
    path('<pk>/connection-detail', ConnectionDetailView.as_view(), name='connection-detail-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('search-connection/', search_connection, name='search-connection'),
    path('check-connection-status/', check_connection_status, name='check-connection-status'),
    path('<slug>/tutor-update-profile/', TutorUpdateView.as_view(), name='tutor-update-profile'),
    path('<slug>/student-update-profile/', StudentUpdateView.as_view(), name='student-update-profile'),
    path('flag-connection/', flag_unflag_connection, name='flag-connection'),
    path('flag-tutor/', flag_unflag_tutor, name='flag-tutor'),
    path('flag-session/', flag_unflag_session, name='flag-session'),
    path('questions/', QuestionListView.as_view(), name='question-list-view'),
    path('action-question/', action_question, name='action-question'),
    path('export-tutoring-tutor-list/', export_tutoring_tutor_list, name='export-tutoring-tutor-list'),
    path('export-tutoring-student-list/', export_tutoring_student_list, name='export-tutoring-student-list'),
    path('export-tutoring-connection-list/', export_tutoring_connection_list, name='export-tutoring-connection-list'),
    path('export-tutoring-session-list/', export_tutoring_session_list, name='export-tutoring-session-list'),
    path('<slug>/profile-note-update-profile', ProfileNoteUpdateView.as_view(), name='profile-note-update-profile'),
    path('<pk>/connection-note-update-profile', ConnectionNoteUpdateView.as_view(), name='connection-note-update-profile'),
    path('search-question/', search_question, name='search-question'),


   
]