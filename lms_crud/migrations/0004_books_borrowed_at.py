# Generated by Django 5.0.4 on 2024-04-18 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms_crud', '0003_alter_books_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='borrowed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
