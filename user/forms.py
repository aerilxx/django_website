from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import Profile, Notebook
from django.contrib.auth.mixins import LoginRequiredMixin

# validate telephone number
import phonenumbers

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
		fields = ("username",
			"first_name",
			"last_name",
			)
		help_texts = {
            'username': None,
        }

		widgets = {
        "first_name":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" , 'required': 'false'}),
		"last_name":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" , 'required': 'false'}),
		"username":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" , 'required': 'false'}),
        }



USER_GENDER = (
		('Male', 'Male'), 
		('Female', 'Female'),
		('Non Binary', 'Non Binary'),
		)
class EditProfileForm(ModelForm):

	class Meta:	
		model = Profile 
		fields = (
			"phone",
			"bio",
			"address",
			"gender",
			"birth_date",
			"concerns",
			"avatar"
	     )
		widgets = {
            "phone":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" ,'required': 'false'}),
			"bio":forms.Textarea(attrs={'class':"form-control",
				'required': 'false','cols':50}),
			"address":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" ,'required': 'false'}),
			"birth_date":forms.TextInput(attrs={'class':"form-control" ,
        	   'type':"text" ,'required': 'false'}),
			"avatar":forms.TextInput(attrs={'type':'file',
				'class':"form-control"}),
			"gender": forms.Select(attrs={'class':'ui-select'}),
			"concerns": forms.Select(attrs={'class':'ui-select'}),
        }

	def clean_phone(self):
		phone = self.cleaned_data['phone']

		if not phone.startswith('+1'):
			phone = "+1"+phone

		x = phonenumbers.parse(phone, None)
		if not phonenumbers.is_valid_number(x):
			raise forms.ValidationError('Please provide a valid phone number.')

			# self._errors['phone'] = self.error_class([ 'Please provide a valid phone number.']) 

		if not phonenumbers.is_possible_number(x):
			self._errors['phone'] = self.error_class(['Too few digits for USA number']) 

		return phone



class CreateNoteForm(ModelForm):

	class Meta:	
		model = Notebook
		fields = ('title','body')
		widgets={
		'title':forms.TextInput(attrs={'class':'notebook_title'}),
		"body":forms.Textarea(attrs={'class':'note'})
		}


