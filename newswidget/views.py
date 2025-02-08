import requests
from django.shortcuts import render

def get_finance_news(request):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'category': 'business',
        'apiKey': 'fa2b8cdd4830452d83db26f7d5472a5b',
        'language': 'en'
    }
    response = requests.get(url, params=params)
    news_data = response.json()

    articles = news_data.get('articles', [])
    return render(request, 'newswidget/newswidget.html', {'articles': articles})
