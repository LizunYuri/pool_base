from django import forms
from .models import CalulateRectangleModel

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