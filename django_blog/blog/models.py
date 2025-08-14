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
