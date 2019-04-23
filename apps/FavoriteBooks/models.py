from django.db import models

from django.db import models
from datetime import date, datetime
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class LoginRegistrationValidator(models.Manager):
    def basicValidators(self, postData):
        errors = {}
        
        if(len(postData["fname"]) < 2):
            errors["firstName"] = "The first name must be greater than 2 characters."

        if(len(postData["lname"]) < 2):
            errors["lastName"] = "The last name must be greater than 2 characters."
        
        today = datetime.now()
        if(postData["birthday"] == ""):
            errors["birthday"] = "The birthday is wrong."
        else:
            birthday = datetime.strptime(postData["birthday"], "%Y-%m-%d").date()
            if(datetime.now().date() < birthday):
                errors["birthday"] = "The birthday is wrong."
            else:
                if((today.year - birthday.year) < 13):
                    errors["birthday"] = "You should be greater than 13 years."
                elif((today.year - birthday.year) == 13):
                    if(today.month < birthday.month):
                        errors["birthday"] = "You should be greater than 13 years."
                    else:
                        if(today.month == birthday.month and today.day < birthday.day):
                            errors["birthday"] = "You should be greater than 13 years."
        
        if(postData["password"] != postData["repassword"] or postData["password"] == "" or len(postData["password"]) < 8):
            errors["password"] = "The Passwords are wrong or short. Minimun 8 characters."

        return errors


    def passwordValidator(self, postData):
        errors = {}
        user = User.objects.filter(user = postData['userLogin'].upper())
        if(user):
            if not bcrypt.checkpw(postData['passwordLogin'].encode(), user[0].password.encode()):
                errors["passwordLogin"] = "Wrong user or password."
        else:
            errors["passwordLogin"] = "Wrong user or password."
            
        return errors, user


    def emailValidator(self, postData):
        errors = {}
        if postData["email"] == "":
            errors["email"] = "Email is required."
        else:
            if not EMAIL_REGEX.match(postData["email"].strip()):
                errors["email"] = "The email is not valid."
            else:
                user = User.objects.filter(email = postData['email'].strip())
                if user:
                    errors["email"] = "Email is already in the data base."

        return errors

    
    def userValidator(self, postData):
        errors = {}
        user = User.objects.filter(user = postData['user'].strip().upper())
        if user:
            errors["user"] = "This user is already in the data base."

        return errors



class booksValidator(models.Manager):
    def validator(self, postData):
        errors = {}
        if(len(postData["title"]) < 3):
            errors["title"] = "The title is too short."
        
        if(len(postData["description"]) < 10):
            errors["description"] = "The description should be greater than 10 characters."

        return errors
        


class User(models.Model):
    #id
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    gender = models.IntegerField()
    birthday = models.DateTimeField()
    email = models.CharField(max_length = 255)
    user = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    objects = LoginRegistrationValidator()
    

class Book(models.Model):
    #id
    title = models.CharField(max_length = 255)
    description  = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
    uploadBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name = "bookUploaded")
    # BE CAREFUL WITH THE VARIABLE NAME WHIT THE RELATIONS MANY TO MANY ---> IT HAS TO BE WHIT PLURAL (s)
    userLikes = models.ManyToManyField(User, related_name = "likesBooks")

    objects = booksValidator()