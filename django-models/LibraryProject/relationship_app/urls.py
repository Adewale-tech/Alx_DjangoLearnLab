from django.urls import path
from .views import list_books, LibraryDetailView
from .views import LibraryDetailView
from .views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),

]
