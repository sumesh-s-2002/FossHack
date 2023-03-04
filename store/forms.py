from dataclasses import field, fields
from django.forms import ModelForm,Form
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm
#creating userform

class RegitrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = ["phone", "profile_pic"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class AddressForm(ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'