from django import forms
from django.contrib.auth.models import User
from .models import Client
from django.contrib import auth


class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','password','email']

class RegisterClientForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['city','university','dormitory','room','phonenumber']



class UserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']










