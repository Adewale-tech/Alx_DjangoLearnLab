from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library  # This line must be here exactly
from .models import UserProfiles
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test

# Role checkers
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin-only view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian-only view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member-only view
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Function-based view for listing books (make sure Book is imported in your models)
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Authentication views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(FormView):
    template_name = 'relationship_app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)