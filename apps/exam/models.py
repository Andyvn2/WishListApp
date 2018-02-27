from __future__ import unicode_literals
import bcrypt
from django.db import models
import re

# Create your models here.
EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX= re.compile(r'^[a-zA-Z]')






class UserManager(models.Manager):
	def basic_validator(self, postData):
		print "running basic_validator"
		errors ={}
		if not NAME_REGEX.match(postData['new_name']):
			errors['new_name']= "Full Name Should only be letters"
		if len(postData['new_name'])<3:
			errors['new_name']="Full Name Should Be More Than Three Letters"
		if not NAME_REGEX.match(postData['new_username']):
			errors['new_username']= "Full Name Should only be letters"
		if len(postData['new_username'])<3:
			errors['new_username']="Full Name Should Be More Than Three Letters"
		if len(postData['new_password']) < 8 :
			errors["new_password"] = "Password is invalid. Must be atleast 8 Characters"
		if not postData["new_password"] == postData["confirm_password"]:
			errors["confirm_password"]= 'Passwords Do Not Match'
		if postData["date"] == "":
			errors['date']= "Please Enter Date Hired"
		if len(errors)==0:
			print "iniate Registration1"
			name=postData["new_name"]
			username=postData["new_username"]
			date_hired= postData["date"]
			print date_hired
			password= bcrypt.hashpw(postData["new_password"].encode(), bcrypt.gensalt())
			User.objects.create(name=name, username=username, password=password, hired_on=date_hired)
			print "Reg Complete"
		return errors
		
		# else:
		# 	print postData["new_name"]
		# if len(errors)==0:
		# 	full_name=postData["new_name"]
		# 	print full_name
			# User.objects.create(name=, alias=)
		# return errors

	def loginValidator(self, postData):
		errors = {}
		if postData["login_username"]== "":
			errors["login_username"]= "Username is Empty"
		elif len(User.objects.filter(username=postData["login_username"]))== 0:
			errors['login_username']= "Username Does not Exist"
		else:
			hash1= User.objects.filter(username=postData["login_username"])[0].password
			if not bcrypt.checkpw(postData["login_password"].encode(), hash1.encode()):
				print "Pw is wrong"
				errors["login_password"]= "Invalid Login"
		if len(errors)==0:
			id=User.objects.filter(username=postData["login_username"])[0].id
			# request.session["alias"]=User.objects.filter(email=postData["login_email"])[0].alias
			# request.session["name"]=User.objects.filter(email=postData["login_email"])[0].name
		return errors

	def item_validator(self, postData):
		errors = {}
		if len(postData["new_item"]) < 3:
			errors['new_item'] = "Please Enter a Valid Item of atleast more than 3 Characters"
		return errors

class User(models.Model):
	name   			= models.CharField(max_length=255)
	username   		= models.CharField(max_length=255)
	password   		= models.CharField(max_length=255)
	hired_on 		= models.CharField(max_length=255)
	created_at   	= models.DateTimeField(auto_now_add = True)
	updated_at   	= models.DateTimeField(auto_now = True)
	objects			=UserManager()

class AddedItem(models.Model):
	new_item 		= models.CharField(max_length=255)
	adder			= models.ForeignKey(User, related_name="items")
	created_at   	= models.DateTimeField(auto_now_add = True)
	updated_at   	= models.DateTimeField(auto_now = True)

class LikedItem(models.Model):
	liked_by		= models.ForeignKey(User, related_name="LikedItems", default="1")
	item			= models.ForeignKey(AddedItem, related_name="LikedItems", default="1")
	created_at   	= models.DateTimeField(auto_now_add = True)
	updated_at   	= models.DateTimeField(auto_now = True)
