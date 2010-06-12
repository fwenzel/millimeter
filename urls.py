from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from lib import base62


admin.autodiscover()

# 404 handler is fine by default
handler500 = 'shortener.views.server_error' # need MEDIA_URL in 500 error.

urlpatterns = patterns('',
    url(r'^$', 'shortener.views.index', name='index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^users/', include('users.urls')),
    (r'^(?P<slug>[%s]+)/$' % base62.VALID_SLUG_CHARS,
     'shortener.views.forward'),
)

# serve media files in debug mode
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

