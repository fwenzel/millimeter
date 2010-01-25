from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from models import Link


def forward(request, slug):
    """The actual forwarder magic"""
    link = get_object_or_404(Link, slug=slug)
    return HttpResponsePermanentRedirect(link.url)

