import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "Chinua Achebe"
books_by_author = Book.objects.filter(author__name=author_name)
print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

# List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}: {[book.title for book in library.books.all()]}")
except Library.DoesNotExist:
    print(f"No library found with name: {library_name}")

# Retrieve the librarian for a library
try:
    librarian = Librarian.objects.get(library__name=library_name)
    print(f"Librarian for {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian found for: {library_name}")
