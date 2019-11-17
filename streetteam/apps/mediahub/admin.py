from django.contrib import admin
from .models import MediaResource


@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    change_form_template = "admin/media_resource_preview.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["image_url"] = MediaResource.objects.get(pk=object_id).resource_url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
