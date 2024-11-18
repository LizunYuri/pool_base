from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
            label='Имя пользователя',
            widget=forms.TextInput(attrs={
                    'class' : 'login-input',
                    'placeholder' : ''
                })
        )
    password = forms.CharField(
            label='Пароль',
            widget=forms.PasswordInput(attrs={
                    'class' : 'login-input',
                    'placeholder' : ''
                })
        )
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # Задать кастомные атрибуты меток
        self.fields["username"].widget.attrs.update({"label_class": "form-label"})
        self.fields["password"].widget.attrs.update({"label_class": "form-label"})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
            ]
        password = forms.CharField(widget=forms.PasswordInput(), required=False)