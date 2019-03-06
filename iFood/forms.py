from django import forms
from django.contrib.auth.models import User
from iFood.models import UserProfile, Feedback, Comments
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter')

class UserDetailsForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_active')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment','created_at')

