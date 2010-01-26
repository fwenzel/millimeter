from django.db.models import F
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

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


