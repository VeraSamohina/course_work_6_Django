from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserRegisterForm, UserForm, UserLoginForm
from users.models import User


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    success_url = reverse_lazy('mailing:index')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Отправка подтверждающего письма на электронную почту для верификации"""
        self.object = form.save()
        text_message = ("Вы успешно зарегистрировались на сайте email-рассылок 'Пульс'. "
                        "Для подтверждения электронной почты перейдите пожалуйста по ссылке")
        id = self.object.id
        url = f"{self.request.build_absolute_uri('verification')}/{id}"
        send_mail(
            subject='Вы зарегистрированы',
            message=f'{text_message} {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False
        )
        return super().form_valid(form)


class VerificationEmailView(TemplateView):
    template_name = 'users/verification.html'

    def get(self, request, *args, **kwargs):
        """Изменение поля на is_verified на True при успешном прохождении верификации"""
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        user.is_verified = True
        user.save()
        return super(VerificationEmailView, self).get(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailing:index')

    def get_object(self, queryset=None):
        """Получение объекта для редактрования"""
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    extra_context = {'title': 'Пользователи сервиса'}
    permission_required = []

    def has_permission(self):
        """Вывод списка пользователей для Модератора"""
        if self.request.user.groups.filter(name='moderator').exists():
            return super().has_permission()


def toggle_users_status(request, pk):
    """Блокировка/разблокировка пользователей модератором"""
    user_groups = [group.name for group in request.user.groups.all()]
    if 'moderator' in user_groups:
        user = User.objects.get(pk=pk)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect(reverse('users:users'))
    else:
        return HttpResponseForbidden('Недостаточно прав для совершения операции')
