from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import localdate
from exam.models import UserData

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
			request.session.set_expiry(86400)
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
		last_username = int(User.objects.order_by("-username")[1].username[5:9])+1
		firstName = request.POST.get('firstName')
		lastName = request.POST.get('lastName')
		email = request.POST.get('email')
		username = str(localdate().year)[2:4]+"103"+str(f"{last_username:04}")
		raw_password = "pass"+request.POST.get('phone')
		user = User.objects.create_user(username=username, password=raw_password, first_name=firstName, last_name=lastName, email=email)
		user = authenticate(username=username, password=raw_password)
		login(request, user)
		messages.add_message(request, messages.SUCCESS, 'Registered Successful')
		userdata = UserData.objects.create(user_name=firstName, user_id=username)
		return redirect('/')
	return render(request, 'signup.html')

def logoutuser(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout Successful')
	return redirect("/")