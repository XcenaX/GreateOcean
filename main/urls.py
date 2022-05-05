from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path('users', views.FriendsView.as_view(), name='users'), 
    path('send_friend_request/<slug:id>', views.SendFriendRequest.as_view(), name='send_friend_request'),
    path('decline_friend/<slug:id>', views.DeclineFriend.as_view(), name='decline_friend'), 
    path('accept_friend/<slug:id>', views.AcceptFriend.as_view(), name='accept_friend'), 
    path('delete_friend/<slug:id>', views.DeleteFriend.as_view(), name='delete_friend'), 
    path("fish/<slug:id>", views.ItemView.as_view(), name="item_description"),
    path("fish/<slug:id>/send_comment", views.SendComment.as_view(), name="send_comment"),
    path("fish/<slug:id>/delete_comment", views.DeleteComment.as_view(), name="delete_comment"),
    path("delete/fish/<slug:id>", views.DeleteItem.as_view(), name="item_delete"),
    path("recover/fish/<slug:id>", views.RecoverItem.as_view(), name="item_recover"),
    path("add/fish", views.AddItem.as_view(), name="item_add"),
    path("edit/fish/<slug:id>", views.EditView.as_view(), name="item_edit"),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
]
#