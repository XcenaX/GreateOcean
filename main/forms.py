from django import forms
from .models import Fish


class FishForm(forms.ModelForm):   
    class Meta:
        model = Fish
        fields = ('name', 'description', "type", "price", "discount", "height", "weight", "image")