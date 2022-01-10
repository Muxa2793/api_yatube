from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all()
        return comments

    def get_serializer_context(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        context = {
            'request': self.request,
            'post': post,
        }
        return context

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        serializer.save(comment=comment, partial=True)

    def perform_destroy(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        comment.delete()
