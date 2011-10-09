import random
from django import forms
from DecisionCandy.app.models import *
from django.forms import ModelForm

class SignUpForm(forms.Form):
  email = forms.EmailField(max_length=30)
  username = email
  password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
  name = forms.CharField(max_length=50, label="Publicly visible name")
  description = forms.CharField()
  
