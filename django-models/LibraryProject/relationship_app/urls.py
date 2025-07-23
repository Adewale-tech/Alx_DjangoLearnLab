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

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
