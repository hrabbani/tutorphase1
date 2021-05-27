from django import forms
from .models import Mentor, Student, Session
from django.forms import TextInput, widgets
from django.forms import DateField




class MentorModelForm(forms.ModelForm):

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'language', 'emergency_contact',
        'employment_status', 'employer_info', 'experience', 'reason', 'support', 'prefer_sex', 'geographical',
        'commit', 'available', 'seminar', 'signature', 'grant', 'check_bridge', 'cont_student_bridge')
        
    def __init__(self, *args, **kwargs):
        super(MentorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


 

class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'grade', 'school',
        'academic_advisor', 'academic_advisor_email', 'reason', 'question1', 'answer1', 'question2', 'answer2',
        'question3', 'answer3', 'prefer_sex', 'geographical', 'commit', 'available', 'seminar', 'signature',)

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('meet', 'length', 'summary', 'help', 'change', 'rate', 'support', 'question', 'cont',)

    def __init__(self, *args, **kwargs):
        super(SessionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




