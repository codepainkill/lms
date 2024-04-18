from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('home/', views.home,name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/',views.custom_logout,name='logout'),
    path('register/',views.register,name='register'),
    path('add_books/',views.add_books,name='add_books'),
    path('rem_books/',views.remove_book,name='rem_books'),
    path('borr_books/',views.borrow_books,name='borr_books'),
    path('borrowed_books/',views.view_borrowed_books,name='borrowed_books'),
    path('return_books/',views.return_books,name='return_books')
]
