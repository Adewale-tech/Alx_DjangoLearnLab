from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name="Chinua Achebe")
books_by_author = Book.objects.filter(author=author)
print("Books by Chinua Achebe:", books_by_author)

# List all books in a library
library = Library.objects.get(name="National Library")
books_in_library = library.books.all()
print("Books in National Library:", books_in_library)

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print("Librarian for National Library:", librarian.name)

