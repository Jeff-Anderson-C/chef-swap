from django import forms
from .models import Image


class ImageForm(foms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')

