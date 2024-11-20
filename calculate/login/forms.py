from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
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


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя',
                                 max_length=150, 
                                 required=True,
                                 widget=forms.TextInput(attrs={'class' : 'profile-form-input',
                                                               'placeholder' : 'Введите имя'})
                                )
    last_name  = forms.CharField(label='Фамилия', 
                                 max_length=150, 
                                 required=True,
                                 widget=forms.TextInput(attrs={'class' : 'profile-form-input',
                                                               'placeholder' : 'Введите имя'})
                                )
    
    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name'
            ]
        
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={'class': 'profile-form-input password-visible', 'placeholder': 'Введите старый пароль'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'profile-form-input password-visible', 'placeholder': 'Введите новый пароль'})
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={'class': 'profile-form-input password-visible', 'placeholder': 'Подтвердите новый пароль'})
    )