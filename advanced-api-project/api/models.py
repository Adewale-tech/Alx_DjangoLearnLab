from django.db import models
from django.db import models

class Author(models.Model):
    """
    Model representing an author.
    Stores the author's name and links to multiple books via a one-to-many relationship.
    """
    name = models.CharField(max_length=100, help_text="Author's full name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Book(models.Model):
    """
    Model representing a book.
    Stores title, publication year, and a reference to its author via ForeignKey.
    """
    title = models.CharField(max_length=200, help_text="Book title")
    publication_year = models.IntegerField(help_text="Year of publication")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author of the book"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

# Create your models here.
