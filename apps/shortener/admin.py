from django.contrib import admin

from models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('slug', 'url', 'visited')
    list_display_links = ('slug', 'url')
    ordering = ('slug',)
admin.site.register(Link, LinkAdmin)

