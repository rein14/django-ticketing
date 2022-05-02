from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cms.forms import BootstrapHelperForm


from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email','roles',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email','roles',)

class UserForm(BootstrapHelperForm, forms.ModelForm):

    class Meta:
        model = User
        fields = ('roles', 'full_names', 'email' )