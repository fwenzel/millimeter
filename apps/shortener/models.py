from django.contrib.auth.models import User
from django.db import IntegrityError, models, transaction

from lib import base62

from .fields import CharNullField


class Link(models.Model):
    """Model representing a single shortened URL"""
    url = models.URLField(max_length=255, verify_exists=False)
    slug = CharNullField(
        blank=True,
        db_index=True,
        default=None,
        help_text='Custom short URL slug. Uses generated ID if empty.',
        max_length=255,
        null=True,
        unique=True,
        verbose_name='short name',
    )
    is_autoslug = models.BooleanField(
        default=False, help_text='was this short name auto-generated?')
    users = models.ManyToManyField(User)
    visited = models.PositiveIntegerField(default=0, editable=False)

    def __unicode__(self):
        return "%s: %s" % (self.slug, self.url)

    def save(self, *args, **kwargs):
        """if the user did not choose a slug, use an auto-generated one"""
        super(Link, self).save(*args, **kwargs)
        if self.slug:
            return

        self.is_autoslug = True
        while True:
            self.slug = AutoSlug.next_autoslug()
            try:
                super(Link, self).save(*args, **kwargs)
                return
            except IntegrityError: # if taken, try again
                pass


class AutoSlug(models.Model):
    """
    Auto-generates unique IDs

    A link in need of a new slug will add a field to AutoSlug, obtain its ID,
    then delete that field. All databases' sequence feature will take care of
    these IDs being unique.
    """
    # we define no fields, so Django's id / pk field will be the only one

    @classmethod
    def next_autoslug(cls):
        """return new unique url slug"""
        iditem = cls()
        iditem.save(force_insert=True)
        newslug = base62.to62(iditem.pk)
        # we can delete all but the highest entry, but need to keep this one
        # around because Django does not use real auto_increment columns on all
        # databases (SQLite, for example). :(
        cls.objects.filter(pk__lt=iditem.pk).delete()
        return newslug

