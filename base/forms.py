from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Resources, ContactUs
from django import forms
from django.forms import formset_factory


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'studentID', 'email', 'name', 'password1', 'password2']



class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','avatar', 'banner', 'resume', 'portfolio',
                   'bio', 'passout_year', 'college', 'branch', 'semester' , 
                   'studentID', 'email', 'phone', 
                   'dob', 'gender', 'address',
                   'linkedIn', 'github', 'instagram']
        


# class AddActivity(forms.Form):
#     name = forms.CharField(max_length=100, label='Task Name')
#     description = forms.CharField(widget=forms.Textarea, label='Description')

# TaskFormSet = formset_factory(TaskForm, extra=1)



class AddResourceForm(ModelForm):
    class Meta:
        model = Resources
        fields = ['name', 'type', 'tags', 'resourcefile', 'size', 'description' ]



class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        # exclude = ['user',]
