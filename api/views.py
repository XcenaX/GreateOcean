
from main.models import *
from rest_framework import viewsets
from api.serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as Auth_User
import secrets
from django.shortcuts import render
from django.core.files import File
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from greate_ocean.settings import BASE_DIR, STATIC_ROOT
from django.db.models import Q

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.template.loader import render_to_string

from django.utils import dateparse
import requests

from rest_framework.permissions import AllowAny

#from .filters import FoundItemFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django.views.decorators.csrf import csrf_exempt

import mimetypes

from django.http import HttpResponse, FileResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from datetime import timedelta
from datetime import date, datetime, timezone

API_KEY = "AIzaSyCcHCB9lx35nurrIOy2KvphPIvmsflB4mE"

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class FishViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["name", "description"]
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Fish.objects.all()
    serializer_class = FishSerializer

    def retrieve(self, request, pk=None):
        queryset = Fish.objects.all()
        try:
            item = Fish.objects.get(id=pk)
            serializer = FishSerializer(item)
            return Response(serializer.data)
        except:
            raise Http404

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        description = self.request.query_params.get('description', None)
        queryset = self.queryset.all()
        query = Q()
        if name is not None:
            query |= Q(name__icontains=name)
        if description is not None:
            query |= Q(description__icontains=description)        
        queryset = queryset.filter(query)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["login", "role"]
    http_method_names = ['get', 'post', 'head', 'put']
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            raise Http404


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ["text", "user__login"]
    http_method_names = ['get', 'post', 'head', 'put']
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        try:
            comment = Comment.objects.get(id=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except:
            raise Http404


class DownloadFile(APIView):
    def get(self, request):
        fl_path = '/file/path'
        filename = 'downloaded_file_name.extension'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        return Response({"error": request.method + " method not allowed!"})

    def post(self, request):
        current_user_id = int(request.POST["current_user"])
        code = request.POST["code"]
        current_user = None
        try:
            current_user = User.objects.get(id=current_user_id)
        except Exception as e:
            return Response({"error": "User with this id nit found!"})
        friend = None
        try:
            friend = User.objects.get(ref_code=code)        
        except Exception as e:
            return Response({"error": "User with this REF CODE nit found!"})
        
        if len(current_user.friends.filter(ref_code=code)) > 0:
            return Response({"error": "Этот человек уже есть в списке друзей"})

        current_user.friends.add(friend)
        friend.friends.add(current_user)
        
        current_user.save()
        friend.save()
        
        return Response({"success": True}) 

