# forms.py
from django import forms
from .models import ClientModel

class ClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['name', 'city', 'phone', 'email', 'responsible', 'note']
