from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, MailingLog
from datetime import datetime, timedelta

current_datetime = datetime.now()


def start_mailing():
    for mailing in Mailing.objects.filter(status='active'):
        if current_datetime >= mailing.end_time:
            mailing.status = 'completed'

        client_emails = [client.email for client in mailing.clients.all()]
        message = mailing.message
        start_time = mailing.start_time

        if start_time <= current_datetime <= mailing.end_time:
            try:
                send_mail(
                    subject=message.title,
                    message=message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=client_emails
                )

                if mailing.period == 'daily':
                    mailing.start_time += timedelta(days=1)
                elif mailing.period == 'weekly':
                    mailing.start_time += timedelta(days=7)
                elif mailing.period == 'monthly':
                    mailing.start_time += timedelta(days=30)
                elif mailing.period == 'one_time':
                    mailing.status = 'completed'
                mailing.save()
                MailingLog.objects.create(attempt_status='success', response='Email sent successfully', mailing=mailing)

            except Exception as e:
                MailingLog.objects.create(attempt_status='error', response=str(e))


def my_write_text():
    with open('txt.txt', 'w') as f:
        f.write('brooo')