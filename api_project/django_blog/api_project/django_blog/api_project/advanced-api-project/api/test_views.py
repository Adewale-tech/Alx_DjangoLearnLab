from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from api.models import Author, Book
from api.serializers import BookSerializer
from django.contrib.auth.models import User

class BookAPITests(APITestCase):
    """
    Test suite for Book model API endpoints.
    Covers CRUD operations, filtering, searching, ordering, and permissions.
    """
    def setUp(self):
        """
        Set up test data: create a user, authors, and books.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book1 = Book.objects.create(
            title="Harry Potter", publication_year=1997, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Chamber of Secrets", publication_year=1998, author=self.author
        )

    def test_list_books(self):
        """
        Test GET /api/books/ to list all books.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        """
        Test GET /api/books/<pk>/ to retrieve a single book.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_authenticated(self):
        """
        Test POST /api/books/create/ with authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'New Book')

    def test_create_book_unauthenticated(self):
        """
        Test POST /api/books/create/ without authentication (should fail).
        """
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_invalid_year(self):
        """
        Test POST /api/books/create/ with future publication year (should fail).
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2026,  # Future year
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_authenticated(self):
        """
        Test PUT /api/books/<pk>/update/ with authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1997,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, 'Updated Harry Potter')

    def test_update_book_unauthenticated(self):
        """
        Test PUT /api/books/<pk>/update/ without authentication (should fail).
        """
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1997,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """
        Test DELETE /api/books/<pk>/delete/ with authenticated user.
        """
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """
        Test DELETE /api/books/<pk>/delete/ without authentication (should fail).
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_title(self):
        """
        Test filtering books by title (?title=Harry).
        """
        url = reverse('book-list') + '?title=Harry'
        response = self.client.get(url)
        books = Book.objects.filter(title='Harry Potter')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_author(self):
        """
        Test filtering books by author ID (?author=1).
        """
        url = reverse('book-list') + f'?author={self.author.pk}'
        response = self.client.get(url)
        books = Book.objects.filter(author=self.author)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_title(self):
        """
        Test searching books by title (?search=Harry).
        """
        url = reverse('book-list') + '?search=Harry'
        response = self.client.get(url)
        books = Book.objects.filter(title__icontains='Harry')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_author_name(self):
        """
        Test searching books by author name (?search=Rowling).
        """
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        books = Book.objects.filter(author__name__icontains='Rowling')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_by_title(self):
        """
        Test ordering books by title (?ordering=title).
        """
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        books = Book.objects.all().order_by('title')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_by_publication_year_desc(self):
        """
        Test ordering books by publication_year descending (?ordering=-publication_year).
        """
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        books = Book.objects.all().order_by('-publication_year')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)