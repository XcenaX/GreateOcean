from datetime import datetime
from django.db import models
from greate_ocean.yandex_s3_storage import ClientDocsStorage

class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comment_user")
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())


class Fish(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0) # скидка в процентах
    height = models.IntegerField(default=0)
    weight  = models.IntegerField(default=0)
    image = models.FileField(storage=ClientDocsStorage())
    deleted = models.BooleanField(default=False)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        return int(self.price * (self.discount/100))


class User(models.Model):
    login = models.TextField(default="")
    password = models.TextField(default="")
    fishes = models.ManyToManyField(Fish, null=True, blank=True)
    role = models.TextField(default="user")
    friends = models.ManyToManyField("User", null=True, blank=True, related_name="user_friends")
    def __str__(self):
        return self.login