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
    path('admin-dashboard/add-user', views.add_user, name='add_user'),
    path('admin-dashboard/delete-user/<int:user_id>', views.delete_user, name='delete_user'),
    path('admin-dashboard/update-user/<int:user_id>', views.update_user, name='update_user'),
    path('admin-dashboard/delete-book/<int:book_id>', views.delete_book, name='delete_book'),
    path('admin-dashboard/update-book/<int:book_id>', views.update_book, name='update_book'),
]