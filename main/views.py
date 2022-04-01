from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404
from django.dispatch import receiver
from django.db.models.signals import *

from main.models import Fish
from cart.cart import Cart

class IndexView(View):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):     
        data = Fish.objects.all()
        length = len(data)
        add_block = (length+1) % 3 == 0 # нужно чтобы добавить пустой блок чтобы все норм отображалось
        cart = Cart(request)
        
        return render(request, self.template_name, {
            "data": data,
            "add_block": add_block,
            "cart": cart,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class ItemView(View):
    template_name = "item-description.html"
    def get(self, request, id):        
        cart = Cart(request)
        fish = None        
        cart_item = None
        try:
            fish = Fish.objects.get(id=id)                     
            cart_item = cart.get_item(fish.id)
        except:
            pass   
        
        return render(request, self.template_name, {
            "item": fish,
            "cart": cart,        
            "cart_item": cart_item,    
        })
    def post(self, request, id):
        return JsonResponse({"error": "POST method not allowed!"})









# Когда в админке удаляем или обновляем фото рыбы нужно удалить ненужное фото из Яндекс бакета
@receiver(post_delete, sender=Fish)
def delete_fish_image_ondelete(sender, instance, using, **kwargs):
    instance.image.delete(save=False)

@receiver(pre_save, sender=Fish)
def delete_fish_image_onsave(sender, instance, using, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    
    new_file = instance.image
    if not old_file == new_file:
        old_file.delete(save=False)

# @receiver(pre_delete, sender=MyImage)
# def myimage_ondelete(sender, instance, using, **kwargs):
#     instance.image.delete(save=False)