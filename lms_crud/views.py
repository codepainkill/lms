# views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm,BookForm,RemoveBookForm,BorrowBookForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseServerError
from .models import Books
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from datetime import timedelta,timezone
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html',{'form':form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your desired page after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request,"login.html")


def custom_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    # Retrieve all records by default

    # Check if the user is authenticated and if there's a search query
    if request.user.is_authenticated:
        records = Books.objects.all()
        search_query = request.GET.get('q')
        if search_query:
            # Filter records based on search query
            records = Books.objects.filter(
                title__icontains=search_query) | \
                      Books.objects.filter(
                          author__icontains=search_query) | \
                      Books.objects.filter(
                          genre__icontains=search_query)

        # Render the template with the records
        return render(request, "home.html", {'records': records})
    else:
        # Render the template with the records
        return render(request, "home.html", {})


@login_required
def add_books(request):
    if request.user.role != 'librarian':
        return HttpResponseForbidden('You do not have permission to access this page.')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')  # Redirect to the home page after adding the book
            except IntegrityError:
                error_message = 'A book with the same title, author, and genre already exists.'
                return HttpResponseBadRequest(error_message)

    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})   


@login_required
def remove_book(request):
    if request.user.role != 'librarian':
        return HttpResponseForbidden('You do not have permission to access this page.')
    
    if request.method == 'POST':
        form = RemoveBookForm(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['book_name']
            book = Books.objects.get(title=book_name)
            book.delete()
            return redirect('home')  # Redirect to the home page after removing the book
    else:
        form = RemoveBookForm()
    return render(request, 'rem_book.html', {'form': form})  


@login_required
def borrow_books(request):
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            try:
                book = form.cleaned_data['book']
                book.availability = False
                book.borrowed_by_id = request.user.id # Populate borrowed_by with the current user's ID
                book.borrowed_at = timezone.now()  # Set borrowed_at to the current date and time
                book.save()                
                book.save()
                messages.success(request, f"{book.title} borrowed successfully.")
                return redirect('home')  # Redirect to home page after borrowing
            except Exception as e:
                print(e)
                return HttpResponseServerError("An error occurred while processing your request.")
    else:
        form = BorrowBookForm()
    return render(request, 'borrow.html', {'form': form})


@login_required
def view_borrowed_books(request):
    borrowed_books = Books.objects.filter(borrowed_by_id=request.user.id)
    print(borrowed_books)
    for book in borrowed_books:
        # Calculate due date as 5 days from borrowed_at
        book.borrowed_at = book.borrowed_at + timedelta(days=5)
    return render(request, "borrowed_books.html", {'borrowed_books': borrowed_books})

@login_required
def return_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Books.objects.get(id=book_id, borrowed_by=request.user)
            # Update book availability and clear borrowed_by and borrowed_at
            book.availability = True
            book.borrowed_by = None
            book.borrowed_at = None
            book.save()
            messages.success(request, f"{book.title} returned successfully.")
        except Books.DoesNotExist:
            messages.error(request, "Book not found or not borrowed by you.")
    return redirect('borrowed_books')