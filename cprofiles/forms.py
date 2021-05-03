from django import forms
from .models import Task, Session
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
        fields = ('meet', 'length', 'topic', 'feedback', 'change', 'support', 'rate', 'question')

    def __init__(self, *args, **kwargs):
        super(SessionModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



