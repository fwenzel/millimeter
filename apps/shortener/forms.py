from django import forms

from models import Link


class ShortenForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('user',)

