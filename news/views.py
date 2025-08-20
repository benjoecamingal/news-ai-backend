from rest_framework import generics
from .serializers import ArticleSerializer, ArticleInstanceSerializer
from .models import Article
from rest_framework.response import Response
from .task import summarize_article

class NewsListView(generics.ListAPIView):
  queryset = Article.objects.all()
  serializer_class = ArticleSerializer

  def get_queryset(self):
    queryset = super().get_queryset()
    category = self.request.query_params.get('category')

    if category:
      queryset = queryset.filter(category__iexact=category)

    return queryset[:50]
  

class SummarizeArticleView(generics.RetrieveAPIView):
  queryset = Article.objects.all()
  serializer_class = ArticleInstanceSerializer

  def retrieve(self, request, *args, **kwargs):
    response = super().retrieve(request, *args, **kwargs)
    article = self.get_object()
    lang = request.query_params.get('lang', 'en')

    print(lang)

    data = response.data

    if lang == 'en' and article.ai_summary_en:
      data['summary'] = article.ai_summary_en
    elif lang == 'tl' and article.ai_summary_tl:
      data['summary'] = article.ai_summary_tl
    else:
      summary = summarize_article(article, lang)
      data['summary'] = summary

    return Response(data)


  

  # def create(self, request, *args, **kwargs):
  #   article = self.get_object()
  #   lang = request.data.get('lang', 'en')

  #   if lang == 'en' and article.ai_summary_en:
  #     return Response({'summary':article.ai_summary_en})
  #   if lang == 'tl' and article.ai_summary_tl:
  #     return Response({'summary':article.ai_summary_tl})
    

    
    summary = summarize_article(article, lang)

    return Response({'summary': summary})
    

    
    
    


