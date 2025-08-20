from openai import OpenAI
import os
from dotenv import load_dotenv
from django.utils import timezone

from django.core.management import call_command



load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= os.getenv('OPEN_ROUTER_API_KEY_ZEB')
)

PROMPT_TEMPLATE = """
You are a professional journalist. Summarize the following Philippine news article into exactly 3 concise bullet points. 
- Each bullet must be under 30 words. 
- Keep it factual and neutral. 
- If 'translate' mode is requested, output only the translated bullet points in conversational Filipino (Tagalog), preserving accuracy. 
- Do not translate unless requested. 
- Return only the bullet points as output, with no explanations, notes, or additional text.


Article:
{article}
"""

def call_openrouter(promt, model='deepseek/deepseek-chat-v3-0324:free', max_tokens=225):
  try:
    completion = client.chat.completions.create(
      model=model,
      messages=[
        {'role': 'system', 'content': 'You are a professional journalist.'},
        {'role': 'user', 'content': promt},
      ],
      temperature=0.2,
      max_tokens=max_tokens
    )
    return completion.choices[0].message.content
  except Exception as e:
    return f'Error generating summary: {str(e)}'
  
def summarize_article(article, lang):
  if lang == 'tl' and article.ai_summary_tl:
    return article.ai_summary_tl    
  if lang == 'en' and article.ai_summary_en:
    return article.ai_summary_en    
  
  text = article.content  
  if len(text) > 3000:
    text = text[:3000]

  promt = PROMPT_TEMPLATE.format(article=text)
  if lang == 'tl':
    promt += "\nTranslate the bullet points to Tagalog after summarizing."

  summary = call_openrouter(promt)

  if lang == 'en':
    article.ai_summary_en = summary
  else:
    article.ai_summary_tl = summary
  article.save()
  return summary


def summarize_new_article(content, lang):     
  text = content  
  if len(text) > 3000:
    text = text[:3000]

  promt = PROMPT_TEMPLATE.format(article=text)
  if lang == 'tl':
    promt += "\nTranslate the bullet points to Tagalog after summarizing."

  summary = call_openrouter(promt)

  return summary


def auto_fetch_news():
  call_command('fetch_news')
  