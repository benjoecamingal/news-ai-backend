from django.urls import path
from .views import NewsListView, SummarizeArticleView

urlpatterns = [
  path('news/', NewsListView.as_view(), name='news-list'),
  path('news/<int:pk>/summarize/', SummarizeArticleView.as_view(), name='news-summarize'),
]