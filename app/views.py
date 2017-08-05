
from django.shortcuts import render

from .forms import RegisterClientForm
from .forms import RegisterUserForm
from .forms import UserLoginForm
from .forms import UploadFileForm
from .forms import RegisterManagerForm

from .models import Client
from .models import University
from .models import Printing

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect
from PyPDF2 import PdfFileReader
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        #проверяем что пользователь не NONE
        if user: 
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
        else:
        	return HttpResponse("Неверный логин или пароль")
                     
    
    else:       
        return render(request,'app/login_page.html')




#представление для загруженного файла

def upload(request):
	if request.method =='POST':
		upload_form = UploadFileForm(request.POST, request.FILES)
		if upload_form.is_valid():
			file = upload_form.cleaned_data.get('file')
			default_storage.save(file.name, ContentFile(file.read()))
			return HttpResponse(PdfFileReader(file).getNumPages())
		

	else:
		upload_form=UploadFileForm()
	return render(request,'app/upload.html',{'upload_form':upload_form})
		
	
#TODO добавить сохранение ссылкак на админа франчайза

def manager_register(request):
	if request.method=='POST':

		manager_form = RegisterManagerForm(request.POST)
		user_form = RegisterUserForm(request.POST)

		if manager_form.is_valid() and user_form.is_valid():
			user=user_form.save()

			manager = manager_form.save(commit=False)
			manager.user = user
			manager.dormitory = manager_form.cleaned_data['dormitory']
			manager.save()
			auth.login(request, user)
			manager_group = Group.objects.get(name='Manager')
			manager_group.user_set.add(user)
			#return HttpResponse("success")			
			
	else:
		manager_form = RegisterManagerForm()
		user_form = RegisterUserForm( )		
	return render(request,'app/manager_register_form.html',{'manager_form':manager_form,'user_form':user_form})




def client_register(request):
	if request.method=='POST':

		client_form = RegisterClientForm(request.POST)
		user_form = RegisterUserForm(request.POST)

		if client_form.is_valid() and user_form.is_valid():

			user=user_form.save()
			client = client_form.save(commit=False)
			client.user = user
			client.city = client_form.cleaned_data.get('city')
			client.university = client_form.cleaned_data['university']
			client.dormitory = client_form.cleaned_data['dormitory']
			client.room = client_form.cleaned_data.get('room')
			client.phonenumber = client_form.cleaned_data.get('phonenumber')
			client.save()
			auth.login(request, user)
			client_group = Group.objects.get(name='Client')
			client_group.user_set.add(user)
			return redirect('/')
						
	else:
		client_form = RegisterClientForm()
		user_form = RegisterUserForm( )		
	return render(request,'app/client_templates/register_page.html',{'client_form':client_form,'user_form':user_form})



@login_required(login_url='/login')
def homepage(request):
	if request.user.groups.filter(name__in=['Client']).exists():
		return render(request,'app/client_templates/homepage.html')

	if request.user.groups.filter(name__in=['Manager']).exists():
		#отправляем форме все заказы прикрепленные за авторизованным менеджером
		query = Printing.objects.filter(manager = request.user.manager)
		return render(request,'app/manager_homepage.html',{'query':query})

	
		

	