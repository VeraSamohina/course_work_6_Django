from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
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
        return self.request.user
