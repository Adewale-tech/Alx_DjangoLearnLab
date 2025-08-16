from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Model representing a blog post.
    Stores title, content, publication date, and author with a one-to-many relationship.
    """
    title = models.CharField(max_length=200, help_text="Title of the blog post")
    content = models.TextField(help_text="Content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="Date when the post was published")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="Author of the blog post"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class Profile(models.Model):
    """
    Model to extend User with additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="User biography")

    def __str__(self):
        return f"{self.user.username}'s profile"

class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who wrote the comment"
    )
    content = models.TextField(help_text="The content of the comment")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date the comment was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date the comment was last updated")

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['created_at']
