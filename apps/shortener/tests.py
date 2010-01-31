import random

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import client, TestCase

from lib import base62

from .models import AutoSlug, Link


class ShortenerTestCase(TestCase):
    """Base TestCase for all Shortener tests"""

    def setUp(self):
        # user and login
        self.username = 'john'
        self.pw = 'johnpw'

        self.user = User.objects.create_user(self.username,
                                             'lennon@thebeatles.com', self.pw)
        self.user.is_staff = True
        self.user.save()
        self.c = client.Client()

    def login(self):
        self.c.login(username=self.username, password=self.pw)


class AutoSlugTest(ShortenerTestCase):
    def test_increasing(self):
        """Are autoslugs increasing?"""
        slug1 = AutoSlug.next_autoslug()
        slug2 = AutoSlug.next_autoslug()
        self.assert_(base62.from62(slug1) < base62.from62(slug2),
                    'slugs must keep increasing')


class LinkTest(ShortenerTestCase):
    def test_autoslug(self):
        """If slug is undefined, will autoslug be assigned?"""
        link = Link(url='http://example.com')
        link.save()
        self.assert_(
            link.slug, 'autoslug must been assigned when slug is undefined')

    def test_autoslug_no_reassignment(self):
        """
        Create a link, delete it, create a new one. Make sure the IDs differ.
        """
        link1 = Link(url='http://example.com')
        link1.save()
        slug1 = link1.slug
        link1.delete()

        link2 = Link(url='http://example.net')
        link2.save()
        slug2 = link2.slug
        self.assertNotEqual(slug1, slug2, 'slugs must not be reassigned')


class ViewTest(ShortenerTestCase):
    def test_forward_valid(self):
        """test if forwarding works"""
        link = Link(url='http://example.com')
        link.save()
        response = self.c.get('%s%s/' % (reverse('index'), link.slug))
        self.assertEqual(response.status_code, 301,
                         'valid URLs lead to 301 redirect')

    def test_forward_invalid(self):
        """accessing an unknown URL slug"""
        response = self.c.get('%s%s/' % (reverse('index'), 'abcdef'))
        self.assertEqual(response.status_code, 404,
                         'invalid URLs lead to 404')

    def test_create_link_unauthorized(self):
        """creating a link via the front page as an anonymous user"""
        myurl = 'http://example.com'

        self.c.post(reverse('index'), {'url': myurl})
        try:
            link = Link.objects.get(url=myurl)
        except Link.DoesNotExist:
            link = None
        self.assertFalse(link,
                         'creating a link via the front page should not work '
                         'for unauthorized users')

    def test_create_link_authorized(self):
        """creating a link via the front page as authorized user"""
        myurl = 'http://example.com'

        self.login()
        self.c.post(reverse('index'), {'url': myurl})
        try:
            link = Link.objects.get(url__startswith=myurl)
        except Link.DoesNotExist:
            link = None
        self.assert_(link, 'creating a link via the front page works')

    def test_create_same_link_with_slug(self):
        """
        creating a link with a slug and without won't map the second request
        to the user-defined slug
        """
        myurl = 'http://example.com/'
        myslug = 'awesome'

        self.login()
        self.c.post(reverse('index'), {'url': myurl, 'slug': myslug})
        self.c.post(reverse('index'), {'url': myurl})

        linkcount = Link.objects.filter(url__exact=myurl).count()
        self.assertEquals(linkcount, 2,
                          'request for the same url should not be mapped to '
                          'the same item if user-defined slug was set')

    def test_create_same_link_without_slug(self):
        """
        creating the same link twice will be mapped to the same item
        """
        myurl = 'http://example.com/'
        self.login()
        self.c.post(reverse('index'), {'url': myurl})
        linkcount = Link.objects.filter(url__exact=myurl).count()
        self.assertEquals(linkcount, 1,
                          'request for the same url witout slug will be '
                          'mapped to the same item')


class StatsTest(ShortenerTestCase):
    def test_count_visits(self):
        """check visit count"""
        link = Link(url='http://example.com')
        link.save()

        visits = random.randint(1, 100)
        for i in range(visits):
            self.c.get('%s%s/' % (reverse('index'), link.slug))
        link = Link.objects.get(pk=link.pk)

        self.assertEqual(visits, link.visited,
                         'number of visits needs to be counted correctly')

