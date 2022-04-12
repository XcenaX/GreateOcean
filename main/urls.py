from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path("fish/<slug:id>", views.ItemView.as_view(), name="item_description"),
    path("delete/fish/<slug:id>", views.DeleteItem.as_view(), name="item_delete"),
    path("add/fish", views.AddItem.as_view(), name="item_add"),
]
#