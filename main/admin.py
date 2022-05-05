from django.contrib import admin
from main.models import *
from rest_framework.authtoken.models import Token

admin.site.register(Fish)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(FriendRequest)
#admin.site.register(Token)