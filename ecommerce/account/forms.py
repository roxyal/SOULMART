from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# Registration Form
class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        # password2 -> is a confirmation password
        fields = ['username', 'email', 'password1', 'password2']

    # *args and **kwargs call allow you to pass any number of positional or keyword arguments to the parent class's
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # By writing this it force email to be required *
        self.fields['email'].required = True

    # Email validation
    def clean_email(self):

        email = self.cleaned_data.get('email')

        # If email is already in our database
        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('This email has already been used')
        
        # Check if the length of email exceeded 350
        if len(email) >= 350:

            raise forms.ValidationError('Your email is too long')
        
        return email

# Login Form
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Update form

class UpdateUserForm(forms.ModelForm):

    password = None

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # By writing this it force email to be required *
        self.fields['email'].required = True

    class Meta:

        model = User

        fields = ['username', 'email'] 
        exclude = ['password1', 'password2']

    # Email validation
    def clean_email(self):

        email = self.cleaned_data.get('email')

        # If email is already in our database
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('This email has already been used')
        
        # Check if the length of email exceeded 350
        if len(email) >= 350:

            raise forms.ValidationError('Your email is too long')
        
        return email

    
