from django.db import models

class Article(models.Model):
  source = models.CharField(max_length=225, blank=True)
  title = models.TextField()
  content = models.TextField()
  url = models.URLField(max_length=2000, blank=True)
  category = models.CharField(max_length=100, blank=True)
  published_at = models.DateTimeField(null=True)
  image_url = models.URLField(max_length=2000, blank=True)
  ai_summary_en = models.TextField(blank=True)
  ai_summary_tl = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-published_at']

  def __str__(self):
    return self.title[:120]
