from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Products



class MultipleImageUploadForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Products.objects.all(), required=True)
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'Multiple': True}),
        required=True
    )   
    
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
