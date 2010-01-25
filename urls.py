from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # (r'^millimeter/', include('millimeter.foo.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^(?P<slug>\w+)/$', 'shortener.views.forward'),
)
