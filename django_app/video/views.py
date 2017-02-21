import requests
from dateutil.parser import parse
from django.shortcuts import render

from youtube.settings import content
from .form import SearchForm
from .models import VideoInfo


def get_search_list_from_youtube(q):
    payload = {
        'part': 'snippet',
        'q': q,
        'type': 'video',
        'maxResults': 50,
        'key': content['youtube']['API_KEY'],
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    raw_dic = r.json()
    items = raw_dic['items']
    result = []
    for item in items:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        published_date_str = item['snippet']['publishedAt']
        published_date = parse(published_date_str)
        info = {
            'title': title,
            'video_id': video_id,
            'published_date': published_date,
        }
        result.append(info)
    return result


def search_youtube(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = request.POST['search']
            items = get_search_list_from_youtube(q)
            for item in items:
                title = item['title']
                video_id = item['video_id']
                published_date = item['published_date']
                VideoInfo.objects.create(
                    video_id=video_id,
                    title=title,
                    published_date=published_date,
                )
            search_result = VideoInfo.objects.filter(title__contains=q).values_list('title', flat=True)
            context = {
                'form': form,
                'search_result': search_result
            }
        return render(request, 'video/search.html', context)

    else:
        form = SearchForm()
    context = {
        'form': form,
    }
    return render(request, 'video/search.html', context)
