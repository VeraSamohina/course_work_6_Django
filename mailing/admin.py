from django.contrib import admin

from mailing.models import Client, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email')

