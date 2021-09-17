from django import forms
from .models import Profile, Session, Connection
from django.forms import TextInput



class TutorModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'grade', 'avatar', 'email', 'subjects', 'languages', 'school', 'student_capacity', 'question', 'age', 'ethnic', 'interest', 'check')


    def __init__(self, *args, **kwargs):
        super(TutorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'student_grade', 'academic_advisor', 'email', 'subjects', 'school', 'parent1_first_name', 'parent1_last_name', 'parent1_phone',
         'parent1_email', 'parent_languages', 'comfortable_share_phone', 'permission_share_grade', 'optional_school_loop_profile_link', 'optional_school_loop_username', 'optional_school_loop_password', 'interest')


    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('meet', 'length', 'subjects', 'help', 'support', 'othersupport', 'rate', 'productivity', 'question', 'disconnect', 'reason_disconnect', 'urgent_check')

    def __init__(self, *args, **kwargs):
        super(SessionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



# class YourLoginForm(LoginForm):
#     def __init__(self, *args, **kwargs):
#         super(YourLoginForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })


class ProfileNoteModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('note',)
        
    def __init__(self, *args, **kwargs):
        super(ProfileNoteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class ConnectionNoteModelForm(forms.ModelForm):

    class Meta:
        model = Connection
        fields = ('note',)
        
    def __init__(self, *args, **kwargs):
        super(ConnectionNoteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
