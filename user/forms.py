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

		widgets = {
        "first_name":forms.TextInput(attrs={'required': 'true','size':50}),
		"last_name":forms.TextInput(attrs={'required': 'true','size':50}),
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
		widgets = {
            "phone":forms.TextInput(attrs={'required': 'true','size':50}),
			"bio":forms.Textarea(attrs={'required': 'true','rows':5, 'cols':50}),
			"address":forms.TextInput(attrs={'required': 'true','size':50}),
			"birth_date":forms.TextInput(attrs={'required': 'true','size':50}),
        }



