
from django.shortcuts import render
from .forms import RegisterClientForm
from .forms import RegisterUserForm
from .forms import UserLoginForm
from .forms import UploadFileForm
from .models import Client
from .models import University
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect
from PyPDF2 import PdfFileReader



def client_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        #проверяем что пользователь не NONE, и что он относится к группе Клиент
        if user and user.client.is_client:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
        else:
        	return HttpResponse("Неверный логин или пароль")
                     
    
    else:       
        return render(request,'app/client_login_page.html')




def manager_login(request):
	pass
	

#представление для загруженного файла

def upload(request):
	if request.method =='POST':
		upload_form = UploadFileForm(request.POST, request.FILES)
		if upload_form.is_valid():
			file = upload_form.cleaned_data.get('file')
			return HttpResponse(PdfFileReader(file).getNumPages())
		

	else:
		upload_form=UploadFileForm()
	return render(request,'app/upload.html',{'upload_form':upload_form})
		
	

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
			
			
			
			
	else:
		client_form = RegisterClientForm()
		user_form = RegisterUserForm( )		
	return render(request,'app/client_register_page.html',{'client_form':client_form,'user_form':user_form})


def client_homepage(request):
	if request.user.is_authenticated and request.user.client.is_client:
		return render(request,'app/client_homepage.html')
	else:
	
		return render(request,'app/client_login_page.html')
	