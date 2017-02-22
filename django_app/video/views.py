import json

import requests
from dateutil.parser import parse
from django.shortcuts import render

from utils.settings import get_setting
from .models import Video


def get_search_list_from_youtube(keyword):
    youtube_api_key = get_setting()['youtube']['API_KEY']
    payload = {
        'part': 'snippet',
        'q': keyword,
        'type': 'video',
        'maxResults': 30,
        'key': youtube_api_key,
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)

    result_dic = r.json()
    items = result_dic['items']

    return items


def search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        items = get_search_list_from_youtube(keyword)
        for item in items:
            youtube_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_date_str = item['snippet']['publishedAt']
            published_date = parse(published_date_str)
            defaults = {
                'title': title,
                'description': description,
                'published_date': published_date
            }
            Video.objects.get_or_create(
                youtube_id=youtube_id,
                defaults=defaults
            )
    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'video/search.html', context)
