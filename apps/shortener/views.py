from django.contrib.sites.models import Site
from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from forms import ShortenForm
from models import Link


def forward(request, slug):
    """The actual forwarder magic"""
    link = get_object_or_404(Link, slug=slug)
    Link.objects.filter(pk=link.pk).update(visited=F('visited')+1) # count visit
    return HttpResponsePermanentRedirect(link.url)


def index(request):
    if not request.user.is_authenticated():
        return render_to_response('index.html', context_instance=
                                  RequestContext(request))
    data = {}
    if request.method == 'POST':
        form = ShortenForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()

            # success data
            current_site = Site.objects.get_current()
            data.update({
                'success': True,
                'long_url': form.cleaned_data['url'],
                'short_url': 'http://%s/%s' % (current_site.domain, link.slug)
            })
    else:
        form = ShortenForm()
    data.update({'form': form})

    return render_to_response('shortener/index.html', data, context_instance =
                              RequestContext(request))

