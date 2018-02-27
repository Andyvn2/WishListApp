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
			request.session["id"]=User.objects.filter(username=request.POST["login_username"])[0].id
			request.session["username"]=User.objects.filter(username=request.POST["login_username"])[0].username
			request.session["name"]=User.objects.filter(username=request.POST["login_username"])[0].name
			print request.session["id"]
			print request.session["name"]
			return redirect('/dashboard')
	return redirect('/')
def home(request):
	if "id" not in request.session:
		print "hacker"
		return redirect('/')
	else:
		context = {
			"user":User.objects.get(id=request.session["id"]),
			"my_likes": LikedItem.objects.filter(liked_by=request.session["id"]),
			"all_likes": AddedItem.objects.exclude(adder_id=request.session["id"])
	}
		print context

	return render(request, "exam/index2.html", context)


def createpage(request):
	if "id" not in request.session:
		print "hacker"
		return redirect('/')
	else:
		return render(request, "exam/create.html")
def NewItem(request):
	if request.method=="POST":
		errors = User.objects.item_validator(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/wish_items/create')
		else:
			print "initiate items"	
			if len(AddedItem.objects.filter(new_item=request.POST["new_item"])):
				this_user = User.objects.get(id=request.session["id"])
				new_item  = AddedItem.objects.filter(new_item=request.POST["new_item"])[0]
				new_like  = LikedItem.objects.create(liked_by=this_user, item=new_item)
				return redirect('/dashboard')
			else:
				this_user = User.objects.get(id=request.session["id"])
				new_item  = AddedItem.objects.create(new_item=request.POST["new_item"], adder=this_user)
				new_like  = LikedItem.objects.create(liked_by=this_user, item=new_item)
				print "new item comepete"
			return redirect('/dashboard')
	return redirect('/wish_items/create')


def remove(request, id):
	a= LikedItem.objects.filter(liked_by=request.session["id"], item=id)
	a.delete()
	return redirect("/dashboard")

def delete(request, id):
	a= AddedItem.objects.filter(adder=request.session["id"], id=id)
	a.delete()
	return redirect('/dashboard')

def item(request, id):
	if "id" not in request.session:
		print "hacker"
		return redirect('/')
	else:
		# if not len(Added.objects.get(id=id).LikedItem.all())
		context={
				"the_item" : AddedItem.objects.get(id=id),
				"this_item": LikedItem.objects.filter(item=id)
				}
		return render(request, "exam/user.html", context)
def add(request,id):
	this_user = User.objects.get(id=request.session["id"])
	new_item  = AddedItem.objects.get(id=id)
	new_like  = LikedItem.objects.create(liked_by=this_user, item=new_item)
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')
# Create your views here.
