from django import forms
from django.contrib.auth.models import User
from iFood.models import UserProfile, Feedback, Comments, Product, Restaurant, Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

#The user form, based on django built-in User Model
#The __init__ helper is a crispy forms form helper
#Used while handling the form at signup
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'E-Mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"8+ characters & please don't use your username as password"}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

#User profile form is an additional form for User signup
#Based on user profile model
#The helper is the same helper as in UserForm
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Food Street'}))
    facebook = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'https://facebook.com/your-name'}))
    twitter = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'https://twitter.com/your-twitter-name'}))
    picture = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter','picture')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

#The user profile edit form is a form for
#Editing user profile details for already registered users
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','facebook','twitter','picture')

#The user profile edit form is a form for
#Editing user details (incl. password) for already registered users
class UserDetailsForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','email','is_active')

#This form handles comments about the website itself
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment','created_at')

class RestaurantFeedback(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('restaurant','comment','user','created_at','rating')
