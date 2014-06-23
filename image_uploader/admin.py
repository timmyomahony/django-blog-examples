from django.contrib import admin

from .models import UploadedImage


class UploadedImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(UploadedImage, UploadedImageAdmin)
