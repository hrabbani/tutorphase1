from django import forms
from .models import Profile, Session
from django.forms import TextInput



class TutorModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'grade', 'avatar', 'email', 'subjects', 'school', 'language', 'student_capacity')


    def __init__(self, *args, **kwargs):
        super(TutorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'grade', 'academic_advisor', 'avatar', 'email', 'subjects', 'school', 'parent1_first_name', 'parent1_last_name', 'parent1_phone',
         'parent1_email', 'parent2_first_name', 'parent2_last_name', 'parent2_phone',
         'parent2_email')


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