from django.db import models
from greate_ocean.yandex_s3_storage import ClientDocsStorage

class Fish(models.Model):
    name = models.TextField(default='')
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0) # скидка в процентах
    height = models.IntegerField(default=0)
    weight  = models.IntegerField(default=0)
    image = models.FileField(storage=ClientDocsStorage())
    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        return int(self.price * (self.discount/100))
