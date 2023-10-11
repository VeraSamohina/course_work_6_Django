from mailing.models import Mailing
from django.core.mail import send_mail
from config import settings



def send_mailing(mailing_id):
    mail_item = Mailing.objects.get(pk=mailing_id)
    client_emails = [client.email for client in mail_item.clients.all()]
    send_mail(mail_item.message.title, mail_item.message.body,
              settings.EMAIL_HOST_USER, client_emails)
