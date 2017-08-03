from django import forms
from django.contrib.auth.models import User
from .models import Client
from .models import Printing
from django.contrib import auth


class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','password','email']


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Имя пользователя'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['password'].label = 'Пароль'
		self.fields['email'].label = 'Email'
        
        
        


class RegisterClientForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['city','university','dormitory','room','phonenumber']

	def __init__(self, *args, **kwargs):
		super(RegisterClientForm, self).__init__(*args, **kwargs)
		self.fields['city'].label = 'Город'
		self.fields['university'].label = 'Университет'
		self.fields['dormitory'].label = 'Общежитие'
		self.fields['room'].label = 'Комната'
		self.fields['phonenumber'].label = 'Номер телефона'



		
class UserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']





class UploadFileForm(forms.ModelForm):
	class Meta:
		model = Printing
		fields = ['fi','is_colored','with_clip','with_clamp']







