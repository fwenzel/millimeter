from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from lib.render import render

from forms import ShortenForm
from models import Link


def forward(request, slug):
    """The actual forwarder magic"""
    link = get_object_or_404(Link, slug=slug)
    Link.objects.filter(pk=link.pk).update(visited=F('visited')+1) # count visit
    return HttpResponsePermanentRedirect(link.url)


@login_required
def index(request):
    current_site = Site.objects.get_current()

    data = {}
    if request.method == 'POST':
        form = ShortenForm(request.POST)
        if form.is_valid():
            try:
                link = Link.objects.filter(url=form.cleaned_data['url'],
                                           is_autoslug=True)[0]
            except IndexError:
                link = form.save()
            link.users.add(request.user)
            link.save()

            # success data
            data.update({
                'success': True,
                'long_url': form.cleaned_data['url'],
                'short_url': 'http://%s/%s' % (current_site.domain, link.slug)
            })
    else:
        # allow pre-populating url with GET (from bookmarklet)
        initial_url = request.GET.get('url', '')

        # no circular bookmarking...
        if initial_url.startswith('http://%s' % current_site.domain):
            initial_url = ''

        form = ShortenForm(initial={'url': initial_url})

    data.update({'form': form})

    return render(request, 'shortener/index.html', data)

