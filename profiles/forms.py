from django import forms
from .models import Profile, Session
from django.forms import TextInput



class TutorModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'eighteen_older', 'not_grade_school', 'grade', 'avatar', 'email', 'subjects', 'languages', 'school', 'student_capacity', 'question')


    def __init__(self, *args, **kwargs):
        super(TutorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'grade', 'academic_advisor', 'email', 'subjects', 'school', 'parent1_first_name', 'parent1_last_name', 'parent1_phone',
         'parent1_email', 'parent_languages', 'comfortable_share_phone', 'permission_share_grade', 'optional_school_loop_profile_link', 'optional_school_loop_username', 'optional_school_loop_password')


    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('meet', 'length', 'subjects', 'feedback', 'elaborate', 'change', 'support', 'othersupport', 'rate', 'question', 'disconnect', 'reason_disconnect')

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