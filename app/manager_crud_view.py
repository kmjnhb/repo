
from django.shortcuts import render
from .forms import UserForm
from .forms import ManagerForm
from .models import Manager
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import View
from django.template.loader import render_to_string


class CreateManager(View):
	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='Franchise admin',login_url='/login'))
	def get(self,request):
		user_form = UserForm()
		manager_form = ManagerForm()
		context = {'manager_form':manager_form,'user_form':user_form}
		block = render_to_string('app/manager/create.html',context = context,request = request)

		data = {'block' :block}
		return JsonResponse (data)
		#return render(request,'app/manager/create.html',{'manager_form':manager_form,'user_form':user_form})


	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='FranchiseAdmin',login_url='/login'))
	def post(self,request):
		manager_form = ManagerForm(request.POST)
		user_form = UserForm(request.POST)
		data = {}
		if manager_form.is_valid() and user_form.is_valid():
			user=user_form.save()
			manager = manager_form.save(commit=False)
			manager.user = user
			manager.dormitory = manager_form.cleaned_data['dormitory']
			manager.save()
			manager_group = Group.objects.get(name='Manager')
			manager_group.user_set.add(user)

		context = {'manager_form':manager_form,'user_form':user_form}
		block = render_to_string('app/manager/create.html',context = context,request = request)

		data = {'block' :block}
		return JsonResponse (data)



		#return render(request,'app/manager/create.html',{'manager_form':manager_form,'user_form':user_form})



class ReadManager(View):
	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='Franchise admin',login_url='/login'))
	def get(self,request,pk):
		manager = get_object_or_404(Manager,pk=pk)
		data = {}
		if manager.fadmin.id != request.user.franchiseadmin.id:
			return HttpResponse(status=403)
			
		data = {'block':render_to_string('app/manager/info.html',
			context={'manager':manager},
			request = request)}
		return JsonResponse(data)






#пока редактирует, если залогинин за менеджера

class UpdateManager(View):
	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='Franchise admin',login_url='/login'))
	def get(self,request,pk):
		manager = get_object_or_404(Manager,pk=pk)
		user = manager.user
		if manager.fadmin.id != request.user.franchiseadmin.id:
			return HttpResponse(status=403)


		user_form = UserForm(instance = user)
		manager_form = ManagerForm(instance = manager)

		context = {'manager_form':manager_form,'user_form':user_form}
		block = render_to_string('app/manager/update.html',context = context,request = request)

		data = {'block' :block}
		return JsonResponse (data)
		#return render(request,'app/manager/update.html',{'manager_form':manager_form,'user_form':user_form})



	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='Franchise admin',login_url='/login'))	
	def post(self,request,pk):
		manager = get_object_or_404(Manager,pk=pk)
		if manager.fadmin.id != request.user.franchiseadmin.id:
			return HttpResponse(status=403)
		user = manager.user
		user_form = UserForm(request.POST,instance = user)
		manager_form = ManagerForm(request.POST,instance = manager)
		data = {}
		if manager_form.is_valid() and user_form.is_valid():
			user_form.save()
			manager_form.save()
			data = {'status':'Updated'}
			return JsonResponse(data)
		else:
			data = {'status':'Not valid form'}
			return JsonResponse(data)





class DeleteManager(View):
	@method_decorator(login_required(login_url='/login'))
	@method_decorator(group_required(group='Franchise admin',login_url='/login'))
	def get(self,request,pk):
		manager = get_object_or_404(Manager,pk=pk)
		if request.user.franchiseadmin.id == manager.fadmin.id:
			manager.user.delete()
			data = {'status':'deleted'}
			return JsonResponse(data)
		else:
			return HttpResponse(status=403)




@login_required(login_url='/login')
@group_required(group = 'Franchise admin')
def manager_list(request):
	query = Manager.objects.filter(fadmin = request.user.franchiseadmin)
	return render(request,'app/manager_list.html',{'query':query})






