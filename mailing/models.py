from django.conf import settings
from django.db import models
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    fullname = models.CharField(max_length=250, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='email')
    comments = models.TextField(verbose_name='комментарии', **NULLABLE)
    birth_day = models.DateField(verbose_name='дата рождения', **NULLABLE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = slugify(self.fullname)
        super().save(*args, **kwargs)


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    body = models.TextField(verbose_name='текст рассылки')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Mailing(models.Model):
    STATUS_CHOICES = [('created', 'created'), ('started', 'started'), ('completed', 'completed')]
    PERIOD_CHOICES = [('one_time', 'one_time'), ('daily', 'daily'), ('weekly', 'weekly'),
                      ('monthly', 'monthly')]
    start_time = models.DateTimeField(verbose_name='начало рассылки', **NULLABLE)
    end_time = models.DateTimeField(verbose_name='конец рассылки', **NULLABLE)
    title = models.CharField(max_length=150, verbose_name='название рассылки')
    period = models.CharField(max_length=15, choices=PERIOD_CHOICES, default='one_time', verbose_name='периодичность')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='created', verbose_name='состояние')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='текст рассылки', **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name='активна')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='пользователь')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='время')
    status = models.CharField(max_length=20, verbose_name='статус')
    response = models.TextField(blank=True, verbose_name='ответ сервера')
