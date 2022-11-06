from asyncio.windows_events import NULL
from xml.parsers.expat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db import models

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )

   

class BasicSignupForm(BaseRegisterForm):
    
    def save(self, request):
            user = super(BaseRegisterForm, self).save(request)
            basic_group = Group.objects.get(name='ordinary')
            basic_group.user_set.add(user)
            return user

class Confirmkey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verif_code = models.CharField(default=NULL, unique=True, max_length=6)
    

    def __str__(self):
        return f'{self.verif_code}, {self.user.username}, {self.user.id}' 