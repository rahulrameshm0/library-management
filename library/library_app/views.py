from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
from . models import Book,Admin, UserBook
from django.contrib.auth import login,logout, authenticate

User  = get_user_model()

# Create your views here.
@login_required
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
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login successfull!")
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Only admin can login!")
                return redirect("admin_login")
        else:
            messages.error(request, "user or password is incorrect!")

    return render(request, "admin-login.html")

def is_admin(user):
    return user.is_authenticated and user.is_staff

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
        
        admin_user = User.objects.create_user(email=email,username=username)
        admin_user.set_password(password)
        admin_user.is_staff = True 
        admin_user.is_superuser = True
        admin_user.save()
        messages.success(request, "Signup successful!")
        return redirect('admin_login')
    return render(request, "admin-signup.html")



def book_list(request):
    books = Book.objects.all()
    return render(request, "library.html", {"books": books})

@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    admin_user = Admin.objects.all()
    users = User.objects.all()
    books = Book.objects.all() 

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

def delete_book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.delete()
    messages.success(request, "Book has been successfully deleted!")
    return redirect("admin_dashboard")

def update_book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        available_copy = request.POST.get("available_copy")

        if not title or not author or not available_copy:
            messages.error(request, "All fields are required!")
            return redirect('admin_dashboard')
        
        if Book.objects.filter(title=title).exclude(id=book_id).exists():
            messages.error(request, "This book already exists")
            return redirect('admin_dashboard')
        
        book_obj.title = title
        book_obj.author = author
        book_obj.available_copy = available_copy
        book_obj.save()

        messages.success(request, "Book has been sucessfully updated")
        return redirect('admin_dashboard')
    
    return render(request, "update_book.html", {"book": book_obj})

User = get_user_model()
@login_required
def purchase_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user 

    if book.available_copy > 0:
        book.available_copy -= 1
        book.save()

        messages.success(request, "Book has been successfully purchased!")
    else:
        messages.error(request, "There are no more copies of this book available!")

    return redirect('library')  

@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user 

    if book.available_copy > 0:
        book.available_copy += 1
        book.save()


        messages.success(request, "Book has been successfully returned!")
    else:
        messages.error(request, "You have not borrowed this book.")

    return redirect('library')

def user_logout(request):  
    logout(request)
    return redirect("login")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def delete_account():
    pass