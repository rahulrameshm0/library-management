from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Book 

from django.contrib.auth import login,logout, authenticate

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfull!")
            return redirect("library")
        else:
            messages.error(request, "user or password is incorrect!")

    return render(request, "user-login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email address already exists!!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists!!")
            return redirect('signup')
        
        users = User.objects.create_user(email=email,username=username,password=password)
        users.save()
        messages.success(request, "Signup successful!")
        return redirect('login')
    
    return render(request, "signup.html")


def book_list(request):
    books = Book.objects.all()
    return render(request, "library.html", {"books": books})  

def sign_out(request):
    pass

def delte_account():
    pass