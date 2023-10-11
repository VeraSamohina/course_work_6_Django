from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from mailing.models import Client, Mailing, Message, MailingLog


def index(request):
    context = {
        'title': 'Сервис управления рассылками'
    }
    return render(request, 'mailing/index.html', context,)


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }


class ClientCreateView(CreateView):
    model = Client
    fields = ('fullname', 'email', 'birth_day', 'comments')
    extra_context = {
        'title': 'Новый клиент',
    }
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('fullname', 'email', 'birth_day', 'comments')
    extra_context = {
        'title': 'Редактирование клиента:'
    }
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        if form.is_valid():
            new_rec = form.save()
            new_rec.slug = slugify(new_rec.fullname)
            new_rec.save()
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {
        'title': 'Удаление клиента'
    }
    success_url = reverse_lazy('mailing:clients')


class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'

    }


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'body')
    extra_context = {
        'title': 'Создание рассылки'
    }
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    model = Message
    fields = ('title', 'body', 'slug')
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    extra_context = {
        'title': 'Удаление рассылки'
    }
    model = Message
    success_url = reverse_lazy('mailing:messages')


class MessageListView(ListView):
    model = Message
    extra_context = {
        'title': 'Тексты для рассылок',

    }


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('title', 'start_time', 'end_time', 'message', 'period', 'status', 'clients')
    success_url = reverse_lazy('mailing:mailings')
    extra_context = {
        'title': 'Создать новую рассылку'
    }


class MailingUpdateView(UpdateView):
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    model = Mailing
    fields = ('title', 'start_time', 'end_time', 'message', 'period', 'status', 'clients')
    success_url = reverse_lazy('mailing:mailings')


class MailingDeleteView(DeleteView):
    extra_context = {
        'title': 'Удаление рассылки'
    }
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')


class MailingLogListView(ListView):
    model = MailingLog


    def get_queryset(self):
        queryset = MailingLog.objects.all()
       # if self.request.user.is_staff:
       #     return Log.objects.all()
       # queryset = Log.objects.filter(mailing__user = self.request.user)
        return queryset


def activate_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.status == 'active':
        mailing_item.status = 'created'
    elif mailing_item.status == 'created':
        mailing_item.status = 'active'
    mailing_item.save()
    return redirect(reverse('mailing:mailings'))


# def test_cron():
#     my_scheduled_print()


