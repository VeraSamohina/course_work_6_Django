from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta, datetime, timezone
from mailing.models import Mailing, MailingLog

current_datetime = datetime.now(timezone.utc)
print(current_datetime)


def send_mailings():
    mailings_completed = Mailing.objects.filter(is_active=True, end_time__lte=current_datetime)
    for mailing in mailings_completed:
        mailing.status = 'completed'
    print(mailings_completed)
    mailing_list = Mailing.objects.filter(is_active=True, status__in=['created', 'started'],
                                          start_time__lte=current_datetime, end_time__gte=current_datetime)
    print(mailing_list)
    for mailing in mailing_list:
        client_emails = [client.email for client in mailing.clients.all()]
        message = mailing.message
        print(f'время в начале прохода {mailing.start_time}')
        try:
            send_mail(
                subject=message.title,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=client_emails,
                fail_silently=False
            )
            log = MailingLog.objects.create(status='success', response='Email sent successfully', mailing=mailing)
            log.save()
            mailing.start_time = log.timestamp
            print(f'время после присваивания времени Log {mailing.start_time}')

            if mailing.period == 'daily':
                mailing.start_time += timedelta(days=1)
                mailing.status = 'started'
            elif mailing.period == 'weekly':
                mailing.start_time += timedelta(days=7)
                mailing.status = 'started'
            elif mailing.period == 'monthly':
                mailing.start_time += timedelta(days=30)
                mailing.status = 'started'
            elif mailing.period == 'one_time':
                mailing.status = 'completed'
            mailing.save()
            print(f' время после mailing(save() {mailing.start_time}')
        except SMTPException as e:
            log = MailingLog.objects.create(status='error', response=str(e), mailing=mailing)
            log.save()
