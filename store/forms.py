from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , SetPasswordForm
from django.contrib.auth.models import User
from .models import *


class Password_updateForm(SetPasswordForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'old_password', 'placeholder': 'Enter your Old Password'}),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'new_password1', 'placeholder': 'Enter your New Password'}),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'new_password2', 'placeholder': 'Confirm your New Password'}),
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class MultipleImageUploadForm(UserChangeForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all(), required=True)
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'Multiple': True}),
        required=True
    )   

class Profile_infoform(forms.ModelForm):
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
    )
    address1 = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
    )
    address2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'City'}),
    )
    state = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'State'}),
    )
    zipcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}),
    )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Country'}),
    )

    class Meta:
        model = Profile
        fields= ('phone','address1','address2','city','state','zipcode','country')


class Profile_updateform(UserChangeForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'Enter your First Name'}),
    )
    
    last_name = forms.CharField(    
        required=True,
        widget=forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Enter your Last Name'}),
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter your Email'}),
    )
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Choose a Username'}),
    )
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super(Profile_updateform, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].label = ""

        for field_name in ['username']:
            self.fields[field_name].help_text = None




    
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'Enter your First Name'}),
    )
    
    last_name = forms.CharField(    
        required=True,
        widget=forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Enter your Last Name'}),
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Enter your Email'}),
    )
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Choose a Username'}),
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Create a Password'}),
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'confirm-password', 'placeholder': 'Confirm your Password'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        # Remove default labels
        for field in self.fields:
            self.fields[field].label = ""

        # Set help texts to empty to prevent Django from adding default hints
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
