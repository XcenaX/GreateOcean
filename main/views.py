from msilib.schema import Font
from django.urls import reverse
from shutil import ExecError
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import *
from matplotlib import image
from matplotlib.pyplot import get

from .modules.functions import *
from main.models import Fish
from cart.cart import Cart
from django.contrib.auth.hashers import make_password, check_password

class LoginView(View):
    template_name = "login.html"
    def get(self, request, *args, **kwargs):                            
        return render(request, self.template_name, {})
    def post(self, request, *args, **kwargs):
        login = post_parameter(request, "login")
        password = post_parameter(request, "password")
        
        user = None
        try:
            user = User.objects.get(login=login)
        except Exception as e:              
            return render(request, self.template_name, {
                "error": "Неверный логин или пароль!"
            })
        if check_password(password, user.password):
            request.session["user"] = user.id
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {
            "error": "Неверный логин или пароль!"
        })

class RegisterView(View):
    template_name = "register.html"
    def get(self, request, *args, **kwargs):                            
        return render(request, self.template_name, {})
    def post(self, request, *args, **kwargs):
        login = post_parameter(request, "login")
        password = post_parameter(request, "password")
        try:
            User.objects.get(login=login) 
            return JsonResponse({"error": "Пользователь уже существует!"})
        except:
            pass

        hash_password = make_password(password)
        user = User.objects.create(login=login, password=hash_password)
        user.save()
        return redirect(reverse("main:login")) # ПОТОМ НУЖНО ИЗМЕНИТЬ ПЕРЕАДЕСАЦИЮ
        

class LogoutView(View):    
    def get(self, request, *args, **kwargs):                            
        return JsonResponse({"error": "GET method not allowed!"})
    def post(self, request, *args, **kwargs):
        del request.session["user"]
        return redirect(reverse("main:login"))

class IndexView(View):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):        
        current_user = get_current_user(request)
        data = Fish.objects.filter(deleted=False)    
        if current_user:
            if current_user.role == "admin":
                data = Fish.objects.all()                        
        cart = Cart(request)
        
        
        return render(request, self.template_name, {
            "data": data,
            "cart": cart,
            "current_user": current_user,
        })
    def post(self, request, *args, **kwargs):
        return JsonResponse({"error": "POST method not allowed!"})

class ItemView(View):
    template_name = "item-description.html"
    def get(self, request, id):                
        cart = Cart(request)
        fish = None        
        cart_item = None
        current_user = get_current_user(request)
        
        try:
            fish = Fish.objects.get(id=id)                     
            cart_item = cart.get_item(fish.id)
        except:
            pass   

        if fish.deleted and current_user.role != "admin":
            return redirect(reverse("main:index"))

        has_permission = False
        
        if current_user:            
            try:
                current_user.fishes.all().get(id=id)
                has_permission = True
            except:
                pass
        
        
        return render(request, self.template_name, {
            "item": fish,
            "cart": cart,        
            "cart_item": cart_item,    
            "current_user": current_user,
            "has_permission": has_permission,
        })
    def post(self, request, id):
        return JsonResponse({"error": "POST method not allowed!"})

class DeleteItem(View):
    def get(self, request):
        return JsonResponse({"error": "Method GET not allowed!"})
    def post(self, request, id):
        current_user = get_current_user(request)
        if current_user:
            if current_user.role != "admin":
                try:
                    current_user.fishes.all().get(id=id)
                except Exception as e:
                    print(e)
                    return redirect(reverse("main:index"))

        try:
            fish = Fish.objects.get(id=id)
            if current_user.role == "user":
                fish.deleted = True
                fish.save()
            elif current_user.role == "admin":
                if fish.deleted:
                    fish.delete()
                else:
                    fish.deleted = True
                    fish.save()

            
            return redirect(reverse("main:index"))
        except Exception as e:
            return JsonResponse({"error": e})

class RecoverItem(View):
    def get(self, request):
        return JsonResponse({"error": "Method GET not allowed!"})
    def post(self, request, id):
        current_user = get_current_user(request)
        if current_user:
            if current_user.role != "admin":                
                return redirect(reverse("main:index"))

        try:
            fish = Fish.objects.get(id=id)            
            fish.deleted = False
            fish.save()            
            return redirect(reverse("main:index"))
        except Exception as e:
            return JsonResponse({"error": e})

class EditView(View):
    template_name = "edit.html"
    def get(self, request, id):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
        try:
            current_user.fishes.all().get(id=id)
        except Exception as e:            
            return redirect(reverse("main:index"))

        fish = None
        cart = Cart(request)
        try:
            fish = Fish.objects.get(id=id)
        except:
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {
            "fish": fish,
            "cart": cart,
            "current_user": current_user,
        })
    def post(self, request, id):

        current_user = get_current_user(request)
        try:
            current_user.fishes.all().get(id=id)
        except Exception as e:
            print(e)
            return redirect(reverse("main:index"))

        cart = Cart(request)
        name = post_parameter(request, "name")
        description = post_parameter(request, "description")
        price = post_parameter(request, "price")
        discount = post_parameter(request, "discount")
        weight = post_parameter(request, "weight")
        height = post_parameter(request, "height")
        image = None
        try:
            image = post_file(request, "image")[0]
        except:
            pass
        
        fish = None
        try:
            fish = Fish.objects.get(id=id)
        except:
            return redirect(reverse("main:index"))
        
        fish.name = name
        fish.price = price
        fish.description = description
        fish.discount = discount
        fish.weight = weight
        fish.height = height
        if image:
            fish.image = image
        fish.save()

        return render(request, self.template_name, {
            "cart": cart,
            "success": "Информация успешно изменена!",
            "fish": fish
        })


class AddItem(View):
    template_name = "item-add.html"
    def get(self, request):
        cart = Cart(request)
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:login"))
    
        return render(request, self.template_name, {
            "cart": cart,           
            "current_user": current_user,
        })
    def post(self, request):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:index"))

        cart = Cart(request)        
        name = post_parameter(request, "name")
        description = post_parameter(request, "description")
        price = post_parameter(request, "price")
        discount = post_parameter(request, "discount")
        weight = post_parameter(request, "weight")
        height = post_parameter(request, "height")
        image = post_file(request, "image")[0]
        

        if not check_image_type(image) or not image:
            return render(request, self.template_name, {
                "cart": cart,           
                "error": "Неверный тип изображения! Разрешены только: jpg, jpeg, png"
            })
        fish = Fish.objects.create(name=name, description=description, price=price, discount=discount, weight=weight, height=height, image=image)
        fish.save()
        return render(request, self.template_name, {
            "cart": cart,           
            "success": "Рыба успешно добавлена!"
        })
        

class SendComment(View):
    def get(self, request):
        return JsonResponse({"error": "Method GET not allowed!"})
    def post(self, request, id):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:index"))
        fish = None
        try:
            fish = Fish.objects.get(id=id)
        except:
            return redirect(reverse("main:index"))

        text = post_parameter(request, "text")
        comment = Comment.objects.create(text=text, user=current_user)
        fish.comments.add(comment)
        fish.save()

        return redirect(reverse("main:item_description", args={id}) + "#comments_block")


class DeleteComment(View):
    def get(self, request):
        return JsonResponse({"error": "Method GET not allowed!"})
    def post(self, request, id):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(reverse("main:index"))
        if current_user.role != "admin":
            return redirect(reverse("main:index"))
        comment = None
        previous = post_parameter(request, "next")
        try:
            comment = Comment.objects.get(id=id)
        except:
            return redirect(reverse("main:index"))        
        comment.delete()
        return redirect(previous + "#comments_block")


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