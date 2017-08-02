from django.shortcuts import render

# Create your views here.
def client_login(request):
	return render(request,'app/client_login_page.html',{})