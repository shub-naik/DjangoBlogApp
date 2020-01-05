from haystack import indexes
from . import models


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr="publish")
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return models.Post

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status__icontains="published")
