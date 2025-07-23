from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library #This line must be here exactly
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

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
        return super().form_valid(form)        from django.shortcuts import render
        from django.views.generic.detail import DetailView
        from .models import Library, Book
        
        # Function-based view
        def list_books(request):
            books = Book.objects.all()
            return render(request, 'relationship_app/list_books.html', {'books': books})
        
        # Class-based view
        class LibraryDetailView(DetailView):
            model = Library
            template_name = 'relationship_app/library_detail.html'
            context_object_name = 'library'
        
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                # Include all books in this specific library
                context['books'] = self.object.books.all()
                return context
    
    def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in the user after registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
