"""
CharNullField from
http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django/1934764#1934764
"""
from django.db import models

class CharNullField(models.CharField):
    description = "CharField that stores NULL but returns ''"

    def to_python(self, value):
        """return django-friendly '' if NULL in DB"""
        if isinstance(value, models.CharField):
            return value
        if value==None:
            return ""
        else:
            return value

    def get_db_prep_value(self, value):
        """Save NULL in DB if field is empty"""
        if value=="":
            return None
        else:
            return value #otherwise, just pass the value

