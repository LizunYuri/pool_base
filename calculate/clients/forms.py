# forms.py
from django import forms
from .models import ClientModel

class ClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = [
            'name', 
            'city', 
            'phone', 
            'email', 
            'responsible', 
            'note'
                ]



class AddClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = [
            'name', 
            'city', 
            'phone', 
            'email', 
            'note'
                ]

    def save(self, commit=True):

        responsible = self.current_user

        instance = super().save(commit=False)
        if responsible:
            instance.responsible = responsible

        if commit:
            instance.save()
        return instance   
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)