from attr import fields
from .models import *
from rest_framework import serializers
from django.core.serializers import serialize
from django.core.files.base import ContentFile
import base64
import six
import uuid
from django.http import Http404, JsonResponse
import json
from main.models import *
from django.contrib.auth.hashers import make_password, check_password

class UserField(serializers.RelatedField):    
    queryset = User.objects.all()
    def to_representation(self, value):
        return value.id
    def to_internal_value(self, data):
        try:
            try:
                return User.objects.get(id=int(data))
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Exception:
            raise serializers.ValidationError(
            'Obj does not exist.'
            )

class CommentSerializer(serializers.ModelSerializer):
    user = UserField(many=False, read_only=False, required=False)
    class Meta:
        model = Comment
        fields = ("id", "text", "user", "created_at")

class FishSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = Fish
        fields = ("id", "name", "description", "weight", "height", "price", "discount", "deleted", "comments")

class FriendSerializer(serializers.ModelSerializer):
    fishes = FishSerializer(many=True, read_only=False, required=False)    
    class Meta:
        model = User
        fields = ("id", "login", "fishes")

class UserSerializer(serializers.ModelSerializer):    
    fishes = FishSerializer(many=True, read_only=False, required=False)    
    friends = FriendSerializer(many=True, read_only=False, required=False)
    class Meta:
        model = User
        fields = ("id", "login", "password", "fishes", "friends")
    
    def create(self, validated_data):        
        try:
            user = User.objects.get(login=validated_data["login"])     
            raise serializers.ValidationError("User alredy exist")                 
        except:
            pass
        login = None
        password = None        
        try:
            login = validated_data['login']
        except:
            pass
        try:
            password = validated_data['password']
        except:
            pass        
        user = User.objects.create(
            login=login,
            password=make_password(password)
        )        
        user.save()
        return user