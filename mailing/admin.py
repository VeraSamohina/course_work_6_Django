from django.contrib import admin

from mailing.models import Client, Mailing, MailingLog, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email')


admin.site.register(MailingLog)
admin.site.register(Mailing)
admin.site.register(Message)