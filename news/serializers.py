from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['id', 'source', 'title', 'content', 'category', 'published_at', 'image_url']


class ArticleInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['id', 'source', 'title', 'content', 'url', 'category', 'published_at', 'image_url', ]