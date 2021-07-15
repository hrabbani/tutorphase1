from django import forms
from .models import Connection, Mentor, Student, Session
from django.forms import TextInput, widgets
from django.forms import DateField




class MentorModelForm(forms.ModelForm):

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'language', 'emergency_contact',
        'employment_status', 'employer_info', 'partner', 'hear', 'experience', 'reason', 'know', 'question1', 'answer1', 'question2', 'answer2', 'support', 'prefer_sex', 'geographical',
        'commit', 'available', 'seminar', 'signature', 'grant', 'cont_student_bridge', 'check', 'spanish', 'question', 'ethnic')
        
    def __init__(self, *args, **kwargs):
        super(MentorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class MentorNoteModelForm(forms.ModelForm):

    class Meta:
        model = Mentor
        fields = ('note',)
        
    def __init__(self, *args, **kwargs):
        super(MentorNoteModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class StudentNoteModelForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('note',)
        
    def __init__(self, *args, **kwargs):
        super(StudentNoteModelForm, self).__init__(*args, **kwargs)
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


 

class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone', 'address', 'grade', 'school',
        'academic_advisor', 'academic_advisor_email', 'reason', 'know', 'question1', 'answer1', 'question2', 'answer2', 'prefer_sex', 'geographical', 'commit', 'available', 'seminar', 'understand', 'signature',)

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('meet', 'dialogue', 'length', 'summary', 'help', 'change', 'rate', 'support', 'question', 'meaningful', 'elaborate', 'urgent', 'urgent_check')

    def __init__(self, *args, **kwargs):
        super(SessionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




