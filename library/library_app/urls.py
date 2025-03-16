from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('library/', views.book_list, name='library'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('library/admin_login/admin_signup/', views.admin_signup, name='admin_signup'),
    path('library/admin_login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/add-book', views.add_book, name='add_book'),
]
