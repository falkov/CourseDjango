from django.contrib import admin

from .models import ContactFormModel


@admin.register(ContactFormModel)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created')
