from django.urls import path
from django.conf.urls import url, include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path("fish/<slug:id>", views.ItemView.as_view(), name="item_description"),
]
#