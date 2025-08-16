from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration, extending UserCreationForm to include email.
    """
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """
    Form for updating Profile model fields.
    """
    class Meta:
        model = Profile
        fields = ['bio']

class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post model instances.
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Enter post content'}),
        }