from random import sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Article
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Client, Mailing, Message, MailingLog
from users.models import User


class HomeView(TemplateView):
    extra_context = context = {'title': 'Главная'}
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        """Получаем общую context_data для всех пользователей и конкретную для авторизованного"""
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing'] = Mailing.objects.all().count()
        context_data['count_active_mailing'] = Mailing.objects.filter(status__in=['created', 'started']).count()
        context_data['count_unique_clients'] = Client.objects.all().distinct().count()
        articles = list(Article.objects.all())
        context_data['random_articles'] = sample(articles, min(3, len(articles)))
        context_data['count_users'] = User.objects.filter(is_active=True, is_staff=False).count()
        user = self.request.user
        if user.is_authenticated:
            context_data['user_count_active_mailing'] = Mailing.objects.filter(status__in=['created', 'started'],
                                                                               owner=user).count()
            context_data['user_count_clients'] = Client.objects.filter(owner=user).count()
            context_data['user_count_messages'] = Message.objects.filter(owner=user).count()
        return context_data


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
        """Присвоение при создании клиента полю 'owner' значения текущего пользователя"""
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
        """Разрешаем редактирование клиента только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    extra_context = {'title': 'Удаление клиента'}
    success_url = reverse_lazy('mailing:clients')

    def get_object(self, queryset=None):
        """Разрешаем удаление клиента только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
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
        """Присвоение при создании рассылки полю 'owner' значения текущего пользователя"""
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
        """Разрешаем редактирование рассылки только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404


class MailingDeleteView(LoginRequiredMixin,  DeleteView):
    extra_context = {'title': 'Удаление рассылки'}
    model = Mailing
    success_url = reverse_lazy('mailing:mailings')

    def get_object(self, queryset=None):
        """Разрешаем удаление рассылки только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Создание сообщения для рассылки'}
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        """Присвоение при создании сообщения полю 'owner' значения текущего пользователя"""
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
        """Разрешаем редактирование сообщения только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
            return self.object
        else:
            raise Http404


class MessageDeleteView(LoginRequiredMixin,  DeleteView):
    extra_context = {'title': 'Удаление рассылки'}
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        """Разрешаем удаление сообщения только пользователю, его создавшему"""
        self.object = super().get_object()
        if self.object.owner == self.request.user:
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


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    extra_context = {'title': 'Статистика рассылок'}

    def get_queryset(self):
        """ Для суперпользователя показываем список всех логов,
                для обычных пользователей получаем список их логов"""
        if self.request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(user=self.request.user)


@login_required
def start_mailing(request, pk):
    """ Переключение статуса рассылки в ручном режиме только для владельца рассылки"""
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if request.user == mailing_item.owner:
        if mailing_item.is_active:
            if mailing_item.status == 'started':
                mailing_item.status = 'created'
            elif mailing_item.status == 'created':
                mailing_item.status = 'started'
            mailing_item.save()
        return redirect(reverse('mailing:mailings'))
    else:
        return HttpResponseForbidden('Недостаточно прав для совершения операции')


@login_required
def deactivate_mailing(request, pk):
    """ Активация/деактивация рассылки для модератора или суперпользователя"""
    mailing_item = get_object_or_404(Mailing, pk=pk)
    user_groups = [group.name for group in request.user.groups.all()]
    if request.user.is_superuser or 'moderator' in user_groups:
        if mailing_item.is_active:
            mailing_item.is_active = False
        else:
            mailing_item.is_active = True
        mailing_item.save()
        return redirect(reverse('mailing:mailings'))
    else:
        return HttpResponseForbidden('Недостаточно прав для совершения операции')
