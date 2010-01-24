from django.contrib.auth.models import User
from django.db import models

class Link(models.Model):
    """Model representing a single shortened URL"""
    url = models.URLField(max_length=255)
    slug = models.CharField(
        blank=True,
        help_text='custom short URL slug. Uses generated ID if empty.',
        unique=True
    )
    user = models.ForeignKey(User)
    visited = models.PositiveIntegerField(default=0, editable=False)

