import re

from django import forms

from lib.base62 import CHARS as BASE62_CHARS

from models import Link


class ShortenForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('user',)

    def clean_slug(self):
        """Make sure slugs only contain valid characters"""
        char_regex = r'^[%s]*$' % BASE62_CHARS
        value = self.cleaned_data['slug']
        if not re.match(char_regex, value):
            raise forms.ValidationError(
                'Short names must only contain alphanumeric characters.'
            )
        return value

