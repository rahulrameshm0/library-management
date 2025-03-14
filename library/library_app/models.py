from django.db import models

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

    def __str__(self):
        return self.title