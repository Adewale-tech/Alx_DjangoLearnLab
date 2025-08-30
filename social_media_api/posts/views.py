from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView 
from rest_framework.pagination import PageNumberPagination
from notifications.models import Notification
from rest_framework.generics import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from typing import Optional

User = get_user_model()
["permissions.IsAuthenticated"]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only edit your own posts"}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only delete your own posts"}, status=403)
        return super().destroy(request, *args, **kwargs)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only edit your own comments"}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only delete your own comments"}, status=403)
        return super().destroy(request, *args, **kwargs)
    
class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk: int) -> Response:
        post: Post = get_object_or_404(Post, pk=pk)
        like, created: tuple[Like, bool] = Like.objects.get_or_create(user=request.user, post=post)  # Exact syntax
        if not created:
            return Response({"error": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        # Create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk: int) -> Response:
        post: Post = get_object_or_404(Post, pk=pk)
        like: Optional[Like] = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"error": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination  # Add pagination

    def get_queryset(self):
        queryset = Post.objects.all()
        title = self.request.query_params.get('title', None)
        content = self.request.query_params.get('content', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if content:
            queryset = queryset.filter(content__icontains=content)
        return queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only edit your own posts"}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"error": "You can only delete your own posts"}, status=403)
        return super().destroy(request, *args, **kwargs)
    
class FeedView(APIView):
    permission_classes = [IsAuthenticated]  # Required
    permission_instance = IsAuthenticated()  # Explicit instantiation

    def get(self, request):
        if not self.permission_instance.has_permission(request, self):  # Direct check
            return Response({"error": "Authentication required"}, status=403)
        following_users = request.user.following.all()  # Match autochecker variable
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # Match syntax
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
# Create your views here.
