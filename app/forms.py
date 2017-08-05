from django import forms
from django.contrib.auth.models import User
from .models import Client
from .models import Printing
from .models import University
from .models import Manager
from .models import FranchiseAdmin
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
        
        
        

#queryset=Contact.objects.none(), widget=forms.CheckboxSelectMultiple()
class RegisterClientForm(forms.ModelForm):
	

	class Meta:
		model = Client
		fields = ['city','dormitory','room','phonenumber','dormitory','university']

	def __init__(self, *args, **kwargs):
		super(RegisterClientForm, self).__init__(*args, **kwargs)
		self.fields['city'].label = 'Город'
		self.fields['dormitory'].label = 'Общежитие'
		self.fields['room'].label = 'Комната'
		self.fields['phonenumber'].label = 'Номер телефона'
		self.fields['university'].widget.attrs = {'class':'form-control'} 
		self.fields['dormitory'].widget.attrs = {'class':'form-control'} 




class FranchiseAdmin(forms.ModelForm):

	class Meta:
		model = FranchiseAdmin
		fields = ['city','university','room','phonenumber']



class RegisterManagerForm(forms.ModelForm):

	class Meta:
		model = Manager
		fields = ['dormitory']

	def __init__(self, *args, **kwargs):
		super(RegisterManagerForm, self).__init__(*args, **kwargs)
		self.fields['dormitory'].widget.attrs = {'class':'form-control'} 

		

			


		
class UserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','password']



class UploadFileForm(forms.ModelForm):
	class Meta:
		model = Printing
		fields = ['file','is_colored','with_clip','with_clamp']







