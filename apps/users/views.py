import hashlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def profile(request):
    data = {}
    # gravatar
    emailhash = hashlib.md5(request.user.email).hexdigest()
    data['gravatar'] = 'http://www.gravatar.com/avatar/%s.jpg?'\
                       'd=identicon' % emailhash

    return render_to_response('registration/profile.html', data,
                              context_instance=RequestContext(request))

