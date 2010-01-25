from django.contrib.auth.models import User
from django.db import models, IntegrityError

from fields import CharNullField
from lib.base62 import to62


class Link(models.Model):
    """Model representing a single shortened URL"""
    url = models.URLField(max_length=255)
    slug = CharNullField(
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


def check_slug(sender, instance, created, **kwargs):
    """if the user did not choose a slug, use an auto-generated one"""
    if instance.slug:
        return
    newslug = instance.autoslug()
    while True:
        instance.slug = newslug
        try:
            instance.save()
            break
        except IntegrityError: # if taken, add an underscore
            newslug += '_'
models.signals.post_save.connect(check_slug, sender=Link)

