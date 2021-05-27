from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



@unauthenticated_user
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        next_url = request.GET.get('next')
        if next_url in ['/', None]:
            if user is not None:
                login(request, user)
                if request.user.groups.all()[0].name == 'tutor':
                    return redirect('profiles:dashboard') 
                if request.user.groups.all()[0].name == 'choice':
                    return redirect('cprofiles:dashboard') 
                if request.user.groups.all()[0].name == 'admin':
                    return redirect('profiles:dashboard')
                if request.user.groups.all()[0].name == 'mentor':
                    return redirect('mprofiles:dashboard') 
            else:
                messages.info(request, 'Username or password is incorrect')

        else:
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_url)

            else:
                messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)



@login_required(login_url='login')
def home_view(request):

    if request.user.groups.all()[0].name == 'tutor':
        return redirect('profiles:dashboard') 
    if request.user.groups.all()[0].name == 'choice':
        return redirect('cprofiles:dashboard') 
    if request.user.groups.all()[0].name == 'admin':
        return redirect('profiles:dashboard') 
    if request.user.groups.all()[0].name == 'mentor':
        return redirect('mprofiles:dashboard') 




def logout_user(request):
	logout(request)
	return redirect('login')