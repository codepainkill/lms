# Generated by Django 5.0.4 on 2024-04-17 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms_crud', '0002_customuser_firstname_customuser_lastname'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='books',
            unique_together={('title', 'author', 'genre')},
        ),
    ]
