from django.core.management import BaseCommand
import os, requests
from django.utils import timezone
from datetime import datetime
from news.models import Article
from dotenv import load_dotenv
from news.task import summarize_new_article

load_dotenv()


NEWS_API_KEY =  os.getenv('NEWS_API_KEY')
NEWS_ENDPOINT = 'https://newsdata.io/api/1/latest'

class Command(BaseCommand):
  help = 'Fetch latest Philippine news and save to DB'

  def handle(self, *args, **options):
    params = {
      'apikey': NEWS_API_KEY,
      'language': 'en',
      'country': 'ph', 
     }
    
    try:
      response = requests.get(NEWS_ENDPOINT, params=params)
      response.raise_for_status()
      data = response.json().get('results', [])

      article_created = 0

      for item in data:
        print(item)
        pub_date = datetime.strptime(item.get('pubDate', ''), '%Y-%m-%d %H:%M:%S')
        pub_date = timezone.make_aware(pub_date)

        content = item.get('description', 'None') or item.get('content', 'None')
        try:
          ai_summary_en = summarize_new_article(content, 'en')
          ai_summary_tl = summarize_new_article(content, 'tl')
        except:
          continue

        _, created = Article.objects.update_or_create(
          url = item.get('link', 'None'),
          defaults={
            'source': item.get('creator', 'None')[0] if item.get('creator') else '',
            'title': item.get('title', 'None'),
            'content': content,
            'category': item.get('category', 'None')[0] if item.get('category') else '',
            'published_at': pub_date,
            'image_url': item.get('image_url', 'None') if item.get('image_url') else '',
            'ai_summary_en': ai_summary_en if ai_summary_en else '',
            'ai_summary_tl': ai_summary_tl if ai_summary_tl else ''
          }
        )

        if created:
          article_created += 1


      
      self.stdout.write(self.style.SUCCESS(f'Successfully imported the news. {article_created} created'))
        

    except Exception as e:
      self.stderr.write(self.style.ERROR(f'News fetch failed: {str(e)}'))
