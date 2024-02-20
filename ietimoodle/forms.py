from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo', widget=forms.TextInput(attrs={'class': 'mb-4 mt-4 ml-[1.4%]'}))
    password = forms.CharField(label='Contraseña', widget=forms.TextInput(attrs={'type': 'password'}))
# myfield = forms.CharField(widget=forms.TextInput(attrs={'class': 'myfieldclass'}))
