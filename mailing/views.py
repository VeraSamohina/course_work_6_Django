from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Client, Mailing, Message, MailingLog


def index(request):
    context = {'title': 'Сервис управления рассылками'}
    return render(request, 'mailing/index.html', context,)


class ClientListView (ListView):
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        """ Для модератора, суперпользователя показываем список всех клиентов,
        для обычных пользователей получаем список созданных им клиентов, иначе пустой список"""
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.request.user.is_superuser or 'moderator' in user_groups:
            return super().get_queryset().all()
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(owner=self.request.user)
        return self.model.objects.none()


class ClientCreateView(LoginRequiredMixin,  CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Новый клиент'}
    success_url = reverse_lazy('mailing:clients')

    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {'title': 'Редактирование клиента:'}
    success_url = reverse_lazy('mailing:clients')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.object.owner != self.request.user or 'moderator' in user_groups:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('mailing:clients')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class MailingListView (ListView):
    model = Mailing
    extra_context = {'title': 'Рассылки'}

    def get_queryset(self):
        """ Для модератора, суперпользователя показываем список всех рассылок,
        для обычных пользователей получаем список созданных им рассылок, иначе пустой список"""
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.request.user.is_superuser or 'moderator' in user_groups:
            return super().get_queryset().all()
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(owner=self.request.user)
        return self.model.objects.none()


class MailingCreateView(LoginRequiredMixin,  CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')
    extra_context = {'title': 'Создать новую рассылку'}

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.instance.owner = self.request.user
            form.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin,  UpdateView):
    extra_context = {'title': 'Редактирование рассылки'}
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailings')

    def get_form_kwargs(self):
        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object()
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.object.owner != self.request.user or 'moderator' in user_groups:
           raise Http404
        return self.object


class MailingDeleteView(LoginRequiredMixin,  DeleteView):
    extra_context = {'title': 'Удаление рассылки'}
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Создание сообщения для рассылки'}
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)




class MessageUpdateView(LoginRequiredMixin,  UpdateView):
    extra_context = {
        'title': 'Редактирование рассылки'
    }
    form_class = MessageForm
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.object.owner != self.request.user or 'moderator' in user_groups:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin,  DeleteView):
    extra_context = {'title': 'Удаление рассылки'}
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class MessageListView (ListView):
    model = Message
    extra_context = {'title': 'Тексты для рассылок'}
    permission_required = 'mailing.view_message'

    def get_queryset(self):
        """ Для модератора, суперпользователя показываем список всех сообщений,
        для обычных пользователей получаем список созданных им рассылок, иначе пустой список"""
        user_groups = [group.name for group in self.request.user.groups.all()]
        if self.request.user.is_superuser or 'moderator' in user_groups:
            return super().get_queryset().all()
        if self.request.user.is_authenticated:
            return super().get_queryset().filter(owner=self.request.user)
        return self.model.objects.none()


class MailingLogListView(ListView):
    model = MailingLog

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


@login_required
def start_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        if mailing_item.status == 'started':
            mailing_item.status = 'created'
        elif mailing_item.status == 'created':
            mailing_item.status = 'started'
        mailing_item.save()
    return redirect(reverse('mailing:mailings'))


@login_required
def deactivate_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_active:
        mailing_item.is_active = False
    else:
        mailing_item.is_active = True
    mailing_item.save()
    return redirect(reverse('mailing:mailings'))


