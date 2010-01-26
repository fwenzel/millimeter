from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'users.views.profile'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^pwchange/$', 'django.contrib.auth.views.password_change'),
    (r'^pwchange/done/$',
        'django.contrib.auth.views.password_change_done'),
    (r'^pwreset/$', 'django.contrib.auth.views.password_reset'),
    (r'^pwreset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^pwreset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm'),
    (r'^pwreset/complete/$',
        'django.contrib.auth.views.password_reset_complete'),
)

