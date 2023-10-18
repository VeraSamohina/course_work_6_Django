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
        """Увеличиваем счетчик просмотров при каждом открытии статьи"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
