from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}, 'index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^users/', include('users.urls')),
    (r'^(?P<slug>\w+)/$', 'shortener.views.forward'),
)

# serve media files in debug mode
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

