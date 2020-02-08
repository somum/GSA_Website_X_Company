from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(destination)
admin.site.register(package)
admin.site.register(wadmin)

class FileInline(admin.TabularInline):
    model = visaInfoFile


class FileAdmin(admin.ModelAdmin):
    inlines = [
        FileInline,
    ]

admin.site.register(visaInfo, FileAdmin)
