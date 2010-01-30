import re

from django import forms

from lib import base62, docstrings

from models import Link


class ShortenForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url', 'slug')

    def clean_slug(self):
        """Make sure slugs only contain valid characters"""
        char_regex = r'^[%s]*$' % base62.VALID_SLUG_CHARS
        value = self.cleaned_data['slug']
        if not re.match(char_regex, value):
            raise forms.ValidationError(docstrings.trim(
                """
                Short names must only contain alphanumeric characters,
                underscores, and dashes.
                """
                ))
        return value

