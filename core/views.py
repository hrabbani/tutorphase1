from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



def home_view(request):

    return redirect('profiles:dashboard') 


