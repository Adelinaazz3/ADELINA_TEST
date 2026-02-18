from django.shortcuts import render
from .models import Posts
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Posts, Comment
from .serializers import PostSerializer, CommentSerializer




@api_view(['GET', 'POST'])
def post_list_api_view(request):

    if request.method == 'GET':
        posts = Posts.objects.filter(is_published=True).annotate(
            comments_count=Count('comments')
        )
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_api_view(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != post.author:
            return Response(
                {"error": "You can edit only your post"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != post.author:
            return Response(
                {"error": "You can delete only your post"},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def comment_list_api_view(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(
            post=post,
            is_approved=True
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                post=post
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail_api_view(request, id):

    comment = get_object_or_404(Comment, id=id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != comment.author:
            return Response(
                {"error": "You can edit only your comment"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != comment.author:
            return Response(
                {"error": "You can delete only your comment"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
