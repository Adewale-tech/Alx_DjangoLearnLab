from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, isAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    View to list all books, with optional filtering by author ID.
    Allows read-only access for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter books by author ID from query parameter.
        Example: /api/books/?author=1
        """
        queryset = super().get_queryset()
        author_id = self.request.query_params.get('author')
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID.
    Allows read-only access for unauthenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new book.
    Requires authentication; uses BookSerializer for validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book by ID.
    Requires authentication; uses BookSerializer for validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book by ID.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
# Create your views here.
