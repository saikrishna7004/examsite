from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
	if request.user.is_anonymous:
		return redirect("login")
	messages.add_message(request, messages.SUCCESS, 'Login Successful')
	return render(request, "index.html")

def loginuser(request):
	if request.method=="POST":
		if not request.POST.get('remember-me', None):
			request.session.set_expiry(0)
		username = request.POST.get("username")
		password = request.POST.get("password")
		rememberme = request.POST.get("rememberme")
		if not rememberme:
			request.session.set_expiry(0)
		else:
			request.session.set_expiry(3600)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("/")
		else:
			messages.add_message(request, messages.WARNING, 'Invalid Username or Password')
			return render(request, "login.html")
	return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logoutuser(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout Successful')
	return redirect("/")