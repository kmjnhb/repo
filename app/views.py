
from django.shortcuts import render
from .forms import RegisterClientForm
from .forms import RegisterUserForm
from .forms import UserLoginForm
from .models import Client
from django.contrib import auth
# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect
def client_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        #проверяем что пользователь не NONE, и что он относиться к группе Клиент
        if user and user.client.is_client:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
        else:
        	pass
            #TODO обработка не правильно логина
           
            

    
    else:       
        return render(request,'app/client_login_page.html')

def client_register(request):
	if request.method=='POST':
		client_form = RegisterClientForm(request.POST)
		user_form = RegisterUserForm(request.POST)
		if client_form.is_valid() and user_form.is_valid():
			
			user = user_form.save()
			user.client.is_client = True
			user.client.city = client_form.cleaned_data.get('city')
			user.client.university = client_form.cleaned_data.get('university')
			user.client.dormitory = client_form.cleaned_data.get('dormitory')
			user.client.room = client_form.cleaned_data.get('room')
			user.client.phonenumber = client_form.cleaned_data.get('phonenumber')
			user.save()
			
	else:
		client_form = RegisterClientForm()
		user_form = RegisterUserForm( )		
	return render(request,'app/client_register_page.html',{'client_form':client_form,'user_form':user_form})


def client_homepage(request):
	if request.user.is_authenticated and request.user.client.is_client:
		return render(request,'app/client_homepage.html')
	else:
	
		redirect(request,'/login') 
	