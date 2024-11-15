from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class registerUserForm(UserCreationForm):
    Email = forms.EmailField(max_length=40, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    First_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class meta():
        model = User
        fields = ('username', 'First_name', 'Last_name', 'Email', 'password1', 'password2', )