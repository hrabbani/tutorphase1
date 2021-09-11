from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.groups.all()[0].name == 'tutor':
				return redirect('profiles:dashboard') 
			if request.user.groups.all()[0].name == 'choice':
				return redirect('cprofiles:dashboard') 
			if request.user.groups.all()[0].name == 'admin':
				return redirect('profiles:dashboard') 
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func



def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			if request.user.groups.exists():

				group_list = []
				for i in request.user.groups.all():
					group_list.append(i.name)

			for j in group_list:
				if j in allowed_roles:
					return view_func(request, *args, **kwargs)

			else:
				return HttpResponse('You are not authorized to view this page')

		return wrapper_func
	return decorator



