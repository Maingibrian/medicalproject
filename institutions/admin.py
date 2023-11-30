from django.contrib import admin
from .models import institution


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("institution_ID", "name", "location",)


admin.site.register(institution, InstitutionAdmin)