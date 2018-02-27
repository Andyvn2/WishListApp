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
		if len(postData['new_name'])<2:
			errors['new_name']="Full Name Should Be More Than Two Letters"
		if not NAME_REGEX.match(postData['new_alias']):
			errors['new_alias']= "Full Name Should only be letters"
		if len(postData['new_alias'])<2:
			errors['new_alias']="Full Name Should Be More Than Two Letters"
		if not EMAIL_REGEX.match(postData['new_email']):
			errors['new_email']= "Email Format is Invalid"
		if len(postData['new_password']) < 8 :
			errors["new_password"] = "Password is invalid. Must be atleast 8 Characters"
		if not postData["new_password"] == postData["confirm_password"]:
			errors["confirm_password"]= 'Passwords Do Not Match'
		if len(errors)==0:
			print "iniate Registration1"
			name=postData["new_name"]
			alias=postData["new_alias"]
			email=postData["new_email"]
			password= bcrypt.hashpw(postData["new_password"].encode(), bcrypt.gensalt())
			User.objects.create(name=name, alias=alias, email=email, password=password)
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
		if postData["login_email"]== "":
			errors["login_email"]= "Email is Empty"
		elif len(User.objects.filter(email=postData["login_email"]))== 0:
			errors['login_email']= "Email Does not Exist"
		else:
			hash1= User.objects.filter(email=postData["login_email"])[0].password
			if not bcrypt.checkpw(postData["login_password"].encode(), hash1.encode()):
				print "Pw is wrong"
				errors["login_password"]= "Invalid"
		if len(errors)==0:
			id=User.objects.filter(email=postData["login_email"])[0].id
			# request.session["alias"]=User.objects.filter(email=postData["login_email"])[0].alias
			# request.session["name"]=User.objects.filter(email=postData["login_email"])[0].name
		return errors


class User(models.Model):
	name   			= models.CharField(max_length=255)
	alias   		= models.CharField(max_length=255)
	email   		= models.CharField(max_length=255)
	password   		= models.CharField(max_length=255)
	created_at   	= models.DateTimeField(auto_now_add = True)
	updated_at   	= models.DateTimeField(auto_now = True)
	objects			=UserManager()