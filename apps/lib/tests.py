import random

from django.test import TestCase

from . import base62


class Base62Test(TestCase):
    """Make sure Base62 converter works as expected"""

    def test_bijective(self):
        """Is base62 conversion working both ways?"""
        numbers = random.sample(xrange(10000000), 60)

        base62ed = map(base62.to62, numbers)
        unbase62ed = map(base62.from62, base62ed)

        for i in range(len(numbers)):
            self.assertEqual(numbers[i], unbase62ed[i])

