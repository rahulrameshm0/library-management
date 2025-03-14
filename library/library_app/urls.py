from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('library/', views.book_list, name='library')
]
