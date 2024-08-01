from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import *

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['GET'])
def user_list_posts(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PostSerializer(user.posts.all(), many = True)
    return Response(serializer.data)

@api_view(['GET'])
def user_list_following(request, pk):
    try:
        profile:Profile = User.objects.get(pk=pk).profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(profile.following.all(), many = True)
    return Response(serializer.data)

@api_view(['GET'])
def user_list_followers(request, pk):
    try:
        profile:Profile = User.objects.get(pk=pk).profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(profile.followers.all(), many = True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_follow(request):
    user = request.user
    
    if 'pk' not in request.data:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    pk = request.data['pk']
    try:
        profile:Profile = User.objects.get(pk=pk).profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    up:Profile=user.profile
    if not up.following.contains(profile):
        up.following.add(profile)
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status= status.HTTP_304_NOT_MODIFIED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_unfollow(request):
    user = request.user
    
    if 'pk' not in request.data:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    pk = request.data['pk']
    try:
        profile:Profile = User.objects.get(pk=pk).profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    up:Profile=user.profile
    if up.following.contains(profile): 
        up.following.remove(profile)
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def posts_create_post(request):
    user = request.user.profile
    
    if 'content' not in request.data:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    content = request.data['content']
    
    post = Post()
    post.content=content
    post.author=user
    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_reply(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user.profile
    
    if 'content' not in request.data:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    content = request.data['content']
    
    reply = Post()
    reply.content=content
    reply.author=user
    reply.reply_to=post
    reply.save()
    serializer = PostSerializer(reply)
    return Response(serializer.data, status= status.HTTP_201_CREATED)

@api_view(['GET'])
def post_list_replies(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PostSerializer(post.replies.all(), many = True)
    return Response(serializer.data)

@api_view(['GET'])
def post_get(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def user_get(request, pk):
    try:
        profile = User.objects.get(pk=pk).profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get_feed(request):
    up:Profile=request.user.profile
    posts=Post.objects.filter(author__followers=up,reply_to=None)
    serializer = PostSerializer(posts, many = True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_like(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user.profile
    
    if not post.likes.contains(user):
        post.likes.add(user)
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status= status.HTTP_304_NOT_MODIFIED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_remove_like(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user.profile
    
    if post.likes.contains(user): 
        post.likes.remove(user)
        return Response(status= status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user.profile
    if post.author==user:
        post.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update_bio(request):
    
    user = request.user
    
    if 'content' not in request.data:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    content = request.data['content']
    
    user.profile.bio=content
    serializer = ProfileSerializer(user.profile)
    return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
