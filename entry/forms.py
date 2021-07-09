from django import forms
from .models import Business, Orders, Customers

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class crearUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
  
     
class orderForm(forms.ModelForm):
    class Meta:
        model= Orders
        fields =[ 'customer','office','odate', 'otime']
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'form-control'}),
            'office': forms.TextInput(attrs={'class': 'form-control'}),
            'odate':forms.DateInput(attrs={'class': 'form-control' }),
            'otime': forms.Select(attrs={'class': 'form-control', 'type': 'time'}),
        }

class customerForm(forms.ModelForm):
    class Meta:
        model= Customers
        fields =[ 'name','email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }