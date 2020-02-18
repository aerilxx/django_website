from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

User._meta.get_field('email')._unique = True

class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2', )

class EditUserForm(ModelForm):

	class Meta:
		model = User
		fields = (
			"first_name",
			"last_name",
			)
		help_texts = {
            'username': None,
        }

class EditProfileForm(ModelForm):

	class Meta:
		model = Profile 
		fields = (
			"phone",
			"bio",
			"address",
			"gender",
			"birth_date",
			"concerns"
	     )

