from django.shortcuts import render, redirect,get_object_or_404
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
    users = User.objects.all() 

    return render(request, 'admin.html', {'admin_user': admin_user, 'books': books, 'users': users})
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
    
def user_list(request):
    users  =User.objects.all()
    return render(request, "user_list.html", {"users": users})

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            messages.error(request, "Please fill all the requierd field")
            return redirect("admin_dashboard")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email address already exist")
            return redirect("admin_dashboard")

        new_user = User.objects.create_user(username=username,email=email, password=password)
        new_user.save()
        messages.success(request, "user has been successfully created!")
        return redirect("admin_dashboard")
    
    return redirect("admin_dashboard")

def delete_book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.delete()
    messages.success(request, "Book has been successfully deleted!")
    return redirect("admin_dashboard")

def delete_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    user_obj.delete()
    messages.success(request, "Book has been successfully deleted!")
    return redirect("admin_dashboard")

def update_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if not username or not email:
            messages.error(request, "All fields are requered!")
            return redirect("admin_dashboard")
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, "This email already exists please try with the different email")
            return redirect('admin_dashboard')
        
        user_obj.username = username
        user_obj.email = email
        user_obj.save()
        messages.success(request, "username and email has been successfully updated")
        return redirect("admin_dashboard") 

    return render(request, "update_user.html", {"user": user_obj})

def update_book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        available_copy = request.POST.get("available_copy")

        if not title or not author or not available_copy:
            messages.error(request, "All fields are required!")
            return redirect('admin_dashboard')
        
        book_obj.title = title
        book_obj.author = author
        book_obj.available_copy = available_copy
        book_obj.save()
        messages.success(request, "Book has been sucessfully updated")
        return redirect('admin_dashboard')
    
    return render(request, "admin.html")


def sign_out(request):
    pass

def delete_account():
    pass