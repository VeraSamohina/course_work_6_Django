from django.db import models
from django.utils.timezone import now


NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='название')
    content = models.TextField(verbose_name='содержание')
    preview = models.ImageField(upload_to='articles/', verbose_name='изображение', **NULLABLE)
    creation_date = models.DateField(default=now, verbose_name='дата создания')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
