from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
from django.db.models import Q

@permission_required('bookshelf.can_view', raise_exception=True)
def view_document(request):
    return HttpResponse("Viewing document")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_document(request):
    return HttpResponse("Creating document")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_document(request):
    return HttpResponse("Editing document")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_document(request):
    return HttpResponse("Deleting document")

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ) if query else Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})