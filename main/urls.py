from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path("fish/<slug:id>", views.ItemView.as_view(), name="item_description"),
    path("delete/fish/<slug:id>", views.DeleteItem.as_view(), name="item_delete"),
    path("add/fish", views.AddItem.as_view(), name="item_add"),
    path("edit/fish/<slug:id>", views.EditView.as_view(), name="item_edit"),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
]
#