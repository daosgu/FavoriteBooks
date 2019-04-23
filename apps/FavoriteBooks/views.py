from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib import messages
from django.http import JsonResponse
import bcrypt
from datetime import datetime, timezone


def index(request):
    return render(request, "FavoriteBooks/index.html")


def create(request):
    if request.method == "POST":
        errors = User.objects.basicValidators(request.POST)
        if(errors):
            for key in errors:
                messages.error(request, errors[key], extra_tags = key)

            return redirect("/")
        else:
            errors = User.objects.emailValidator(request.POST)
            if(errors):
                for key in errors:
                    messages.error(request, errors[key], extra_tags = key)
                
                return redirect("/")
            else:
                errors = User.objects.userValidator(request.POST)
                if(errors):
                    for key in errors:
                        messages.error(request, errors[key], extra_tags = key)
                    
                        return redirect("/")
                else:
                    hashPassword = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
                    user = User.objects.create(
                        firstName = request.POST["fname"].upper(),
                        lastName = request.POST["lname"].upper(),
                        birthday = request.POST["birthday"],
                        gender = request.POST["gender"],
                        email = request.POST["email"].strip(),
                        user = request.POST["user"].upper(),
                        password = hashPassword.decode(),
                    )
                    request.session["id"] = user.id
                    request.session["firstName"] = user.firstName
                    request.session["lastName"] = user.lastName
                    return redirect("/load")


def login(request):
    if request.method == "POST":
        errors, user = User.objects.passwordValidator(request.POST)
        if(errors):
            for key in errors:
                messages.error(request, errors[key], extra_tags = key)
            return redirect("/")
        else:
            request.session["id"] = user[0].id
            request.session["firstName"] = user[0].firstName
            request.session["lastName"] = user[0].lastName
            return redirect("/load")
    else:
        return redirect("/")


def load(request):
    try:
        if request.session["id"]:
            books = Book.objects.all().order_by("title")
            user = User.objects.get(id = request.session["id"])
            context = {
                "books": books,
                "user": user,
            }
            return render(request, "FavoriteBooks/books.html", context)
    except:
        return redirect("/")



def logOutUser(request):
    try:
        del request.session["id"]
        del request.session["firstName"]
        del request.session["lastName"]
    except:
        print("Error when the user close session.")
    # When the user logOut and the session is clear and the function is redirect to load, the button back allways reload de Login 
    # This way works to cancel de back button when the user close session
    return redirect("/load")



def checkUser(request):
    errors = {}
    errors = User.objects.userValidator(request.POST)
    if len(errors) > 0 :
        for key in errors:
            messages.error(request, errors[key], extra_tags = key)
        
    data = {
        "errors": errors,
        "url": "/",
    }
    return JsonResponse(data)


def checkEmail(request):
    errors = {}
    errors = User.objects.emailValidator(request.POST)
    if len(errors) > 0 :
        for key in errors:
            messages.error(request, errors[key], extra_tags = key)
        
    data = {
        "errors": errors,
        "url": "/",
    }
    return JsonResponse(data)



def createBook(request):
    if request.method == "POST": 
        errors = {}
        errors = Book.objects.validator(request.POST)
        if(len(errors) > 0):
            for key in errors:
                messages.error(request, errors[key], extra_tags = key)
        else:
            user = User.objects.get(id = request.session["id"])
            book = Book.objects.create(
                title = request.POST["title"],
                description = request.POST["description"],
                uploadBy = user
            )
            book.userLikes.add(user)

    return redirect("/load")



def showFor(request, idBook):
    book = Book.objects.get(id = idBook)
    likes = book.userLikes.all()
    user = User.objects.get(id = request.session["id"])
    context = {
        "book": book,
        "likes": likes,
        "user": user
    }
    return render(request, "FavoriteBooks/update.html", context)


def addFavorite(request, idBook):
    book = Book.objects.get(id = idBook)
    user = User.objects.get(id = request.session["id"])
    user.likesBooks.add(book)
    return redirect("/load")


def unFavorite(request, idBook):
    book = Book.objects.get(id = idBook)
    user = User.objects.get(id = request.session["id"])
    user.likesBooks.remove(book)
    return redirect("/load")


def updateBook(request, idBook):
    errors = {}
    book = Book.objects.get(id = idBook)
    if request.method == "POST": 
        if(len(request.POST["description"]) < 10):
            errors["description"] = "The description should be greater than 10 characters."

        if(len(errors) > 0):
            for key in errors:
                messages.error(request, errors[key], extra_tags = key)
        else:
            user = User.objects.get(id = request.session["id"])
            book.description = request.POST["description"]
            book.updated_at = datetime.now(timezone.utc)
            book.save()

    return redirect("/load")


def deleteBook(request):
    pass