from django import forms
from django.contrib.auth.models import User
from iFood.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter')

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter')

class UserDetailsForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_active')
