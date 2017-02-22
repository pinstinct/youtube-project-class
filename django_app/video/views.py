import requests
from dateutil.parser import parse
from django.shortcuts import render

from utils.settings import get_setting


def search_from_youtube(keyword, page_token=None):
    youtube_api_key = get_setting()['youtube']['API_KEY']
    payload = {
        'part': 'snippet',
        'q': keyword,
        'type': 'video',
        'maxResults': 5,
        'key': youtube_api_key,
    }
    if page_token:
        payload['pageToken'] = page_token
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    result_dic = r.json()

    return result_dic


def search(request):
    videos = []
    context = {
        'videos': videos,
    }
    keyword = request.GET.get('keyword', '').strip()
    page_token = request.GET.get('page_token')
    if keyword != '':
        result_dic = search_from_youtube(keyword, page_token)
        prev_page = result_dic.get('prevPageToken')
        next_page = result_dic.get('nextPageToken')
        context['prev_page'] = prev_page
        context['next_page'] = next_page
        context['keyword'] = keyword

        items = result_dic['items']
        for item in items:
            youtube_id = item['id']['videoId']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_date_str = item['snippet']['publishedAt']
            published_date = parse(published_date_str)

            item_dict = {
                'youtube_id': youtube_id,
                'thumbnail': thumbnail,
                'title': title,
                'description': description,
                'published_date': published_date,
            }
            videos.append(item_dict)
    return render(request, 'video/search.html', context)
