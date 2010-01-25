from django.contrib import admin

from models import Link


class LinkAdmin(admin.ModelAdmin):
    ordering = ('id',)
admin.site.register(Link, LinkAdmin)

