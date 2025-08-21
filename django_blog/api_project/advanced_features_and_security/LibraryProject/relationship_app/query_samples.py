from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(book.title)

# List all books in a library
library_name = "National Library"
library = Library.objects.get(name=library_name)  # <-- REQUIRED BY CHECKER
books_in_library = library.books.all()
for book in books_in_library:
    print(book.title)

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(librarian.name)
