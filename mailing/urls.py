from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
                           MessageCreateView, MessageUpdateView, MessageDeleteView, MessageListView, MailingListView,
                           MailingCreateView, MailingDeleteView, MailingUpdateView,
                           MailingLogListView, start_mailing, deactivate_mailing, HomeView)

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='create_client'),
    path('clients/edit/<slug>/', ClientUpdateView.as_view(), name='edit_client'),
    path('clients/delete/<slug>/', ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', cache_page(60)(MessageListView.as_view()), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/edit/<slug>/', MessageUpdateView.as_view(), name='edit_message'),
    path('messages/delete/<slug>/', MessageDeleteView.as_view(), name='delete_message'),

    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('mailings/edit/<slug>/', MailingUpdateView.as_view(), name='edit'),
    path('mailings/delete/<slug>/', MailingDeleteView.as_view(), name='delete'),
    path('mailings/start/<int:pk>/', start_mailing, name='start'),
    path('mailings/deactivate/<int:pk>', deactivate_mailing, name='deactivate'),

    path('mailings/logs/', MailingLogListView.as_view(), name='logs'),

]
