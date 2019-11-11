from django.contrib import admin
from .models import MediaResource


class MediaResourceAdmin(admin.ModelAdmin):
    pass


admin.site.register(MediaResource, MediaResourceAdmin)
