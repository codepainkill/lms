# models.py
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    USER_ROLE = 'user'
    LIBRARIAN_ROLE = 'librarian'
    ROLE_CHOICES = (
        (USER_ROLE, 'User'),
        (LIBRARIAN_ROLE, 'Librarian'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER_ROLE)
    firstname = models.CharField(max_length=30,null=True, blank=True)
    lastname = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return self.username
    
class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, default=None)
    borrowed_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        # Add a unique constraint to ensure no duplicate books based on title, author, and genre
        unique_together = [['title', 'author', 'genre']]

    def __str__(self):
        return self.title
