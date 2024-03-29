from django import forms
from .models import Image



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')



class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50)
	last_name = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)