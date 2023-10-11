from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, index,
                           MessageCreateView, MessageUpdateView, MessageDeleteView, MessageListView, MailingListView,
                           MailingCreateView, MailingDeleteView, MailingUpdateView, activate_mailing,
                           LogListView)

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('receivers/', ClientListView.as_view(), name='clients'),
    path('receivers/create/', ClientCreateView.as_view(), name='create_client'),
    path('receivers/edit/<slug>/', ClientUpdateView.as_view(), name='edit_client'),
    path('receivers/delete/<slug>/', ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/edit/<slug>/', MessageUpdateView.as_view(), name='edit_message'),
    path('messages/delete/<slug>/', MessageDeleteView.as_view(), name='delete_message'),

    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('mailings/edit/<slug>/', MailingUpdateView.as_view(), name='edit'),
    path('mailings/delete/<slug>/', MailingDeleteView.as_view(), name='delete'),
    path('mailings/start/<int:pk>/', activate_mailing, name='start'),
    # path('mailings/test/', test_cron, name='test_cron'),

    path('mailings/logs/', LogListView.as_view(), name='logs'),

]
