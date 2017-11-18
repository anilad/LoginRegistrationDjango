from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[^0-9]+$')
PASSWORD_REGEX = re.compile(r"^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")

class UserManager(models.Manager):
    def valCreate(self, postData):
        errors=[]
        bday = datetime.strptime(postData['birthdate'], '%Y-%m-%d')
        numResults = User.objects.filter(email=postData['email'])
        if len(numResults) > 0:
            errors.append("Unable to register")
            return (False, errors)
        # set up check for empty form to return errors 
        if len(postData['fName'])<1 and len(postData['lName'])<1 and len (postData['email'])<1 and len(postData['birthdate'])<1 and len(postData['pwd'])<1:
            errors.append("Please fill out the form to register")
            return (False, errors)
        if len(postData['fName'])<2:
            errors.append("First name is required")
        elif not NAME_REGEX.match(postData['fName']):
            errors.append("Invalid first name")
        if len(postData['lName'])<2:
            errors.append("Last name is required")
        elif not NAME_REGEX.match(postData['lName']):
            errors.append("Invalid last name")
        if postData['email'] == "":
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email")
        if postData['birthdate']=="":
            errors.append("Birthdate is required")
        else:
            today=datetime.today()
            if (today-bday).days/365<18:
                errors.append("Unable to register: User must be 18 years or older")
        print postData['birthdate']
        if postData['pwd'] == "":
            errors.append("Password is required")
        elif not PASSWORD_REGEX.match(postData['pwd']):
            errors.append("Invalid password")
        if postData['pwd'] != postData['confirm']:
            errors.append("Password does not match password confirmation")
        if len(errors)==0:
            # update create to include all fields from form
            hashed = bcrypt.hashpw(postData['pwd'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=postData['fName'], last_name=postData['lName'], email=postData['email'],birthday=bday, password = hashed)
            return (True, user)
        else:
            return (False, errors)

    def valLogin(self,postData):
        errors=[]
        if postData['email']=="" and postData['pwd']=="":
            errors.append("Please fill out the form to login")
            return (False, errors)
        if postData['email']=="":
            errors.append("Email is required")
        elif postData['pwd']=="":
            errors.append("Password is required")
        elif len(postData['pwd'])>15:
            errors.append("Password is too long")
        if not User.objects.filter(email=postData['email']) or not User.objects.filter(password=postData['pwd']):
            errors.append("Incorrect email or password")
        if len(errors)!=0:
            return (False, errors)
        else:
            user = self.get(email=postData['email'])
            return (True, user)

# updated User to accomodate all form input from client
class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    birthday=models.DateField(null=True, blank=True)
    password=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
