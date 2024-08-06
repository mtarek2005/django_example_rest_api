from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class PostSerializer(serializers.ModelSerializer):
    likes_count =serializers.IntegerField()
    class Meta:
        model = Post
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"username","first_name","last_name",]

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'