from django.shortcuts import render
from .forms import RegisterClientForm
from .forms import RegisterUserForm
# Create your views here.
def client_login(request):
	return render(request,'app/client_login_page.html')

def client_register(request):
	if request.method=='POST':
		client_form = RegisterClientForm(request.POST)
		user_form = RegisterUserForm(request.POST)
		if client_form.is_valid() and user_form.is_valid():
			
			user = user_form.save()
			user.client.city = client_form.cleaned_data.get('city')
			user.client.university = client_form.cleaned_data.get('university')
			user.client.dormitory = client_form.cleaned_data.get('dormitory')
			user.client.room = client_form.cleaned_data.get('room')
			user.client.phonenumber = client_form.cleaned_data.get('phonenumber')
			user.save()
			
	else:
		client_form = RegisterClientForm(instance=request.user)
		user_form = RegisterUserForm( instance=request.user.client)		
	return render(request,'app/client_register_page.html',{'client_form':client_form,'user_form':user_form})




