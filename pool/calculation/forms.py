from django import forms
from .models import CalulateRectangleModel
from clients.models import ClientModel


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = [
                'name',
                'city',
                'phone',
                'email',
                'note',
            ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
                'class' : 'client-name-input'
            })
        self.fields['city'].widget.attrs.update({
                'class' : 'client-name-input'
            })
        self.fields['phone'].widget.attrs.update({
                'class' : 'client-name-input'
            })
        self.fields['email'].widget.attrs.update({
                'class' : 'client-name-input'
            })
        # self.fields['note'].widget.attrs.update({
        #         'class' : 'client-name-note'
        #     })


class CalulateRectangleForm(forms.ModelForm):
    class Meta:
        model = CalulateRectangleModel
        fields = [
            'client',
            'length', 
            'width', 
            'depth_from', 
            'depth_to',
            'water_exchange_time', 
            'filtration_speed'
            ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({
                'class' : 'client-name-note'
            })
        self.fields['length'].widget.attrs.update({
                'class' : 'client-name-note'
            })
        self.fields['width'].widget.attrs.update({
                'class' : 'client-name-note'
            })
        self.fields['depth_from'].widget.attrs.update({
                'class' : 'client-name-note'
            })
        self.fields['depth_to'].widget.attrs.update({
                'class' : 'client-name-note'
            })
        self.fields['water_exchange_time'].widget.attrs.update({
                'class' : 'client-name-input'
            })
        self.fields['filtration_speed'].widget.attrs.update({
                'class' : 'client-name-input'
            })