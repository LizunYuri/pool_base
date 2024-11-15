from django import forms
from .models import SupplierModel

class CreateSupplierModelForm(forms.ModelForm):
    class Meta:
        model = SupplierModel
        fields = [
                'name',
                'legal_name',
                'email',
                'manager',
                'phone',
                'url'
            ]