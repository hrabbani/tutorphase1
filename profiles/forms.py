from django import forms
from .models import Profile, Subject
# from allauth.account.forms import LoginForm

class ProfileModelForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'age', 'avatar', 'email', 'subjects', 'school')


    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)
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