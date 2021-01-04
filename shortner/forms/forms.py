from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username':forms.TextInput(attrs={'class': 'input-field',  'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'id':'email','class': 'input-field', 'type': 'email', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'id':'f_name','class': 'input-field', 'placeholder': 'Enter First Name', 'required' :'required'}),
            'last_name': forms.TextInput(attrs={'id':'l_name','class': 'input-field', 'placeholder': 'Enter Last Name' ,'required' :'required'}),
            'password1': forms.PasswordInput(attrs={'id':'pass_1','class': 'input-field', 'placeholder': 'Enter Password' }),
            'password2': forms.PasswordInput(attrs={'id':'pass_2','class': 'input-field','placeholder':'Confirm Password'}),
        }

