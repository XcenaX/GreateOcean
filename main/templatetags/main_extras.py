
from django import template
register = template.Library()
from ..models import FriendRequest

@register.filter
def has_friend_request(obj, user):
    for req in FriendRequest.objects.all():
        if req.owner == obj and req.user == user:
            return True
        elif req.user == obj and req.owner == user:
            return True
    return False