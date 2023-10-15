from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Article


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = {
            'object_list': Article.objects.all(),
            'title': 'БЛОГ'
        }
        return context


class ArticleDetailView(DetailView):
    model = Article


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        article_item = Article.objects.get(pk=self.kwargs.get('pk'))
        context_data['article_pk'] = article_item.pk
        context_data['title'] =  article_item.title
        return context_data

