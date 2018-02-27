from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import *


def index(request):
	return render(request, "exam/index.html")
def register(request):
	print "creating new account"
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
		else:
			print "initiate register"
			return redirect('/')
	return redirect('/')
def login(request):
	if request.method == "POST":
		errors = User.objects.loginValidator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')
		else:
			request.session["id"]=User.objects.filter(email=request.POST["login_email"])[0].id
			request.session["alias"]=User.objects.filter(email=request.POST["login_email"])[0].alias
			request.session["name"]=User.objects.filter(email=request.POST["login_email"])[0].name
			print request.session["id"]
			print request.session["name"]
			return redirect('/home')
	return redirect('/')
def home(request):
	return render(request, "exam/index2.html")
# Create your views here.
