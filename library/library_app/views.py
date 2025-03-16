from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Book,Admin

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

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfull!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "user or password is incorrect!")

    return render(request, "admin-login.html")

def admin_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email address already exists!!")
            return redirect('admin_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists!!")
            return redirect('admin_signup')
        
        users = User.objects.create_user(email=email,username=username,password=password)
        users.save()
        messages.success(request, "Signup successful!")
        return redirect('admin_login')
    return render(request, "admin-signup.html")

def book_list(request):
    books = Book.objects.all()
    return render(request, "library.html", {"books": books})

def admin_dashboard(request):
    admin_user = Admin.objects.all()
    books = Book.objects.all()

    return render(request, 'admin.html', {'admin_user': admin_user, 'books': books})

def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        available_copy = request.POST.get("available_copy")

        if title and author and available_copy.isdigit():
            Book.objects.create(title=title, author=author, available_copy=int(available_copy))
            messages.success(request, "book successfully added!")
        else:
            messages.error(request, "Please fill all fields")
        
        return redirect("admin_dashboard")

def delete_book(request):
    pass

def sign_out(request):
    pass

def delete_account():
    pass