from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'What\'s up?'}))
    sender = forms.EmailField(required=True, label='email address', widget=forms.TextInput(attrs={'placeholder': 'Enter your Email Address'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}))
    cc_myself = forms.BooleanField(required=False, label="Want me to send you a copy of this message?")
