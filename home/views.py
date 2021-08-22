from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import localdate
from .models import UserVerifyData
from exam.models import UserData
import random

# Create your views here.

def index(request):
	if request.user.is_anonymous:
		return redirect("login")
	messages.add_message(request, messages.SUCCESS, 'Login Successful')
	return render(request, "index.html")

def loginuser(request):
	if not request.user.is_anonymous:
		return redirect("/")
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
			verified = UserVerifyData.objects.filter(username=username)[0].verified
			if verified:
				login(request, user)
				return redirect("/")
			else:
				messages.add_message(request, messages.WARNING, 'Invalid Username or Password')
				return redirect("verify")
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
		messages.add_message(request, messages.SUCCESS, 'Registered Successful. Your username is '+str(username)+'. Verify your identity <a href="verify">Here</a>.')
		userdata = UserData.objects.create(user_name=firstName, user_id=username)
		userverifydata = UserVerifyData.objects.create(username=username, verified=False, otp=random.randint(100000, 999999))
		return render(request, 'signup.html')
	return render(request, 'signup.html')

def verify(request):
	if not request.user.is_anonymous:
		return redirect("/")
	if request.method == 'POST':
		username = request.POST.get('username')
		otp = request.POST.get('otp')
		userverifydata = UserVerifyData.objects.filter(username=username)[0]
		if int(otp) == int(userverifydata.otp):
			userverifydata.verified=True
			userverifydata.save()
			messages.add_message(request, messages.SUCCESS, 'User Verified Successfully')
			return redirect('login')
		else:
			messages.add_message(request, messages.WARNING, 'OTP Incorrect')
			return render(request, 'verify.html')
	return render(request, 'verify.html')

def logoutuser(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Logout Successful')
	return redirect("/")