# forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Books
from django import forms
from datetime import datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'firstname','lastname','email', 'password1', 'password2', 'role']

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'genre']

class RemoveBookForm(forms.Form):
    book_name = forms.CharField(label='Book Name')

    def clean_book_name(self):
        book_name = self.cleaned_data['book_name']
        if not Books.objects.filter(title=book_name).exists():
            raise forms.ValidationError("Book with this name does not exist.")
        return book_name
    
'''class BorrowBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Books.objects.filter(availability=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].empty_label = "Select Book"'''

class BorrowBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Books.objects.filter(availability=True))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].empty_label = "Select Book"

    def save(self, user):
        book_instance = self.cleaned_data['book']
        book_instance.availability = False
        book_instance.borrowed_by = user
        book_instance.borrowed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        book_instance.save()