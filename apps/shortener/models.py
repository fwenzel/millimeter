from django.contrib.auth.models import User
from django.db import models, IntegrityError

from lib.base62 import to62


class Link(models.Model):
    """Model representing a single shortened URL"""
    url = models.URLField(max_length=255)
    slug = models.CharField(
        blank=True,
        db_index=True,
        default=None,
        help_text='Custom short URL slug. Uses generated ID if empty.',
        max_length=255,
        null=True,
        unique=True
    )
    user = models.ForeignKey(User)
    visited = models.PositiveIntegerField(default=0, editable=False)

    def autoslug(self):
        """return id-based url slug"""
        return to62(self.id)

    def __unicode__(self):
        return "%s: %s" % (self.slug, self.url)

    def save(self, *args, **kwargs):
        """if the user did not choose a slug, use an auto-generated one"""
        if self.slug:
            super(Link, self).save(*args, **kwargs)
            return

        self.slug = self.autoslug()
        while True:
            try:
                super(Link, self).save(*args, **kwargs)
                return
            except IntegrityError: # if taken, add an underscore
                self.slug += '_'

