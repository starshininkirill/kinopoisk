from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Логин'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите имя пользователя'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Введите пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Повторите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input'
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input'
    }), required=False)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'file-input'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'readonly': True
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-input'
    }), required=False)
    
    class Meta:
        model = User
        fields = ('username', 'avatar', 'first_name', 'last_name', 'email')