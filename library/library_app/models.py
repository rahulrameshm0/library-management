from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=150, null=True, unique=True)
    username = models.CharField(max_length=150, null=True, unique=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    available_copy = models.IntegerField(default=1)

    def __str__(self):
        return self.title



class AdminLogin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True, null=True)
    password = models.CharField(max_length=150)

    def __str__(self):
        return f"Admin: {self.username}"


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin: {self.user.username}"
    
    def add_book(self, title, author, copies=5):
        return Book.objects.create(title=title, author=author, copies=copies)
    
    def delete_book(self, book_id):
        book = Book.objects.get(id=book_id)
        book.delete()

    def update_book(self, book_id, title=None, author=None, copies=None):
        book = Book.objects.get(id=book_id)
        if title:
            book.title = title
        if author:
            book.author = author
        if copies is not None:
            book.copies = copies
        book.save()

    def add_user(self, username, email, password):
        return User.objects.create(username=username,password=password, email=email)
    
    def delete_user(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()

