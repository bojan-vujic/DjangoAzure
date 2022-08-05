from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'date_created', )
    search_fields = ['file_name', ]


admin.site.register(File, FileAdmin)