from django import forms
from .models import Task, Session, Mentor, Student, Parentsession, Connection
from django.forms import TextInput, widgets
from django.forms import DateField



# class TaskModelForm(forms.ModelForm):

#     class Meta:
#         model = Task
#         fields = ('task1', 'task2', 'task3', 'task4', 'task5', 'task6', 'task7', 'task8', 'task9', 'task10', 'task1date', 'task2date',
#                     'task3date', 'task4date', 'task5date', 'task6date', 'task7date', 'task8date',
#                     'task9date', 'task10date', 'task1status', 'task2status', 'task3status', 'task4status', 
#                     'task5status', 'task6status', 'task7status', 'task8status', 'task9status', 'task10status') 

#     task1date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task2date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task3date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task4date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task5date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task6date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task7date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task8date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task9date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))
#     task10date = DateField(input_formats=["%d %b %Y"], required=False, widget=forms.DateInput(format=('%d %b %Y'),))

#     def __init__(self, *args, **kwargs):
#         super(TaskModelForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })
        





class TaskModelForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('task1status', 'task2status', 'task3status', 'task4status', 
                    'task5status', 'task6status', 'task7status', 'task8status', 'task9status', 'task10status') 

    def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        



class SessionModelForm(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('meet', 'length', 'topic', 'feedback', 'change', 'support', 'rate', 'question', 'elaborate', 'productivity', 'urgent_check')

    def __init__(self, *args, **kwargs):
        super(SessionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



class MentorModelForm(forms.ModelForm):

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'avatar', 'prefer_grade', 'prefer_gender', 'prefer_location', 'mentor_last_year', 'language', 'experience', 'familiar', 'share', 'hobby', 'question', 'ethnic') 

    def __init__(self, *args, **kwargs):
        super(MentorModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class StudentModelForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'gender', 'grade', 'school', 'language_preference', 'parent1_first_name', 'parent1_last_name', 'parent1_phone',
         'parent1_email', 'activity', 'ind_scl', 'dont_know', 'proud', 'learn', 'happy', 'hobby', 'int_ind_school', 'look_ind_school', 'strength', 'obstacle', 'child_strength', 'social_strength', 'interview_language', 'question',  'question1', 'answer1', 'question2', 'answer2')

    def __init__(self, *args, **kwargs):
        super(StudentModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




class ParentSessionModelForm(forms.ModelForm):

    class Meta:
        model = Parentsession
        fields = ('meet', 'length', 'topic', 'share', 'change', 'question', 'urgent_check')

    def __init__(self, *args, **kwargs):
        super(ParentSessionModelForm, self).__init__(*args, **kwargs)
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