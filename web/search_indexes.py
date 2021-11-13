from haystack import indexes
from web import models


class ArchivesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='title')
    keywords = indexes.NgramField(model_attr='keywords')
    description = indexes.NgramField(model_attr='description')
    article_body = indexes.CharField()

    def get_model(self):
        return models.Archives

    # 外键表
    def prepare_body(self, obj):
        return obj.article.body

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
