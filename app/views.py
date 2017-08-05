
from django.shortcuts import render

from .forms import RegisterClientForm
from .forms import RegisterUserForm
from .forms import UserLoginForm
from .forms import UploadFileForm
from .forms import RegisterManagerForm

from .models import Client
from .models import University
from .models import Printing
from .models import Manager

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
	return render(request,'app/client/upload.html',{'upload_form':upload_form})
		
	


def client_create(request):
	if request.method=='POST':

		client_form = RegisterClientForm(request.POST)
		user_form = RegisterUserForm(request.POST,instance=request.user)

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
		user_form = RegisterUserForm()		
	return render(request,'app/client/create.html',{'client_form':client_form,'user_form':user_form})




@login_required(login_url='/login')
def homepage(request):
	if request.user.groups.filter(name__in=['Client']).exists():
		return render(request,'app/client/homepage.html')

	if request.user.groups.filter(name__in=['Manager']).exists():
		#отправляем форме все заказы прикрепленные за авторизованным менеджером
		query = Printing.objects.filter(manager = request.user.manager)
		return render(request,'app/manager/homepage.html',{'query':query})

	if request.user.groups.filter(name__in=['Franchise admin']).exists():
		#отправляем форме все заказы прикрепленные за авторизованным менеджером
		query = Manager.objects.filter(fadmin = request.user.franchiseadmin)
		return render(request,'app/manager_list.html',{'query':query})




from django.views import View

	
		
class ManagerView(View):
	def post(self,request):
		manager_form = RegisterManagerForm(request.POST)
		user_form = RegisterUserForm(request.POST)

		if manager_form.is_valid() and user_form.is_valid():
			user=user_form.save()
			manager = manager_form.save(commit=False)
			manager.user = user
			manager.dormitory = manager_form.cleaned_data['dormitory']
			manager.save()
			manager_group = Group.objects.get(name='Manager')
			manager_group.user_set.add(user)


		else:
			manager_form = RegisterManagerForm()
			user_form = RegisterUserForm( )		
		return render(request,'app/manager/create.html',{'manager_form':manager_form,'user_form':user_form})


#context={'manager_form':manager_form,'user_form':user_form}
#form = render_to_string('app/manager/create.html',       context,request=request,)
#return JsonResponse({'form'=form})


	def update(self,request,pk):
		user = get_object_or_404(User,pk =pk)
		manager_form = RegisterManagerForm(request.POST,instance = user.manager)
		user_form = RegisterUserForm(request.POST,user)

		if manager_form.is_valid() and user_form.is_valid():
			user_form.save()
			manager_form.save()
		
		else:
			manager_form = RegisterManagerForm()
			user_form = RegisterUserForm( )		
		return render(request,'app/manager/create.html',{'manager_form':manager_form,'user_form':user_form})



	def get(self,request):
		if request.user.groups.filter(name__in=['Franchise admin']).exists():
		#отправляем форме все заказы прикрепленные за авторизованным менеджером
			query = Manager.objects.filter(fadmin = request.user.franchiseadmin)
			return render(request,'app/manager_list.html',{'query':query})
		return HttpResponse(status = 401)
#TODO проверка на авторизацию, и то, что менеджер относится к админу

	def delete(self,request,pk):
		manager = get_object_or_404(Manager,pk =pk)
		manager.delete()
		return HttpResponse('Opereation succeed')





















	