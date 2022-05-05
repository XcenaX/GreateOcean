from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import *

from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter()
router.register(r'fishes', FishViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet)

from rest_framework.authtoken import views as api_views

urlpatterns = [
    url(r'^', include(router.urls)),        
    path('api-token-auth/', api_views.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)