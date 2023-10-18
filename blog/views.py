from django.views.generic import ListView, DetailView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    extra_context = {'title': 'БЛОГ'}


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при каждом открытии статьи"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
