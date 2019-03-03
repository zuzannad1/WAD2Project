from django import forms
from django.contrib.auth.models import User
from iFood.models import UserProfile

class UserProfile(forms.ModelForm):
    username = forms.CharField(label = ('Username'), max_length = 30)
    fullname = forms.CharField(label = ('Full Name'), max_length = 30)  
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(label = ('E-Mail Address'), max_length = 128)
    address = forms.CharField(label = ('Address'), max_length =128)
    
    class Meta:
        model = User
        fields = ('username','fullname','password','email','address')
        
                      
