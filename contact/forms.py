from django import forms


class ContactForm(forms.Form):
    contact_subject = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'class':"form-control" ,
               'type':"text" , 'id': 'subject', 'placeholder':'Subject'}))
    contact_name = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'class':"form-control" ,
               'type':"text" , 'id': 'name', 'placeholder':'Your Name'}))
    contact_email = forms.EmailField(required=True,
        widget=forms.TextInput(attrs={'class':"form-control" ,
               'type':"text" , 'id': 'email','placeholder':'Your Email'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class':"form-control w-100" ,
               'type':"text" , 'id': 'message' , 'cols':"30", 'rows':"9", 
               'placeholder':'Enter Message'}))
