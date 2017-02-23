import requests
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from member.models import BookmarkVideo
from utils.settings import get_setting
from video.models import Video


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
    # redirectd을 위해 경로 확인해보기
    # print(request.path_info)
    # print(request.path)
    # 요청해온 URL 정보를 가져온다. (GET 파라미터 포함)
    # print(request.get_full_path())

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
            # 이미 북마크에 추가된 영상인지 판단
            is_exist = BookmarkVideo.objects.filter(
                user=request.user,
                video__youtube_id=youtube_id
            ).exists()

            item_dict = {
                'youtube_id': youtube_id,
                'thumbnail': thumbnail,
                'title': title,
                'description': description,
                'published_date': published_date,
                'is_exist': is_exist,
            }
            videos.append(item_dict)
    return render(request, 'video/search.html', context)


@login_required
def bookmark_toggle(request):
    def get_or_create_video_and_add_bookmark():
        defaults = {
            'title': title,
            'description': description,
            'published_date': published_date,
            'url_thumbnail': url_thumbnail
        }
        video, _ = Video.objects.get_or_create(
            defaults=defaults,
            youtube_id=youtube_id
        )
        # 중간자 모델 없이 M2M 필드에 바로 인스턴스를 추가할 때
        # request.user.bookmark_videos.add(video)

        # BookmarkVideo 중간자 모델의 매니저를 직접 사용
        # BookmarkVideo.objects.create(
        #     user=request.user,
        #     video=video
        # )

        # MyUser와 중간자모델을 연결시켜주는 related_manager를 사용
        # 위의 방법과 동일하게 동작
        request.user.bookmarkvideo_set.create(
            video=video
        )
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        youtube_id = request.POST['youtube_id']
        url_thumbnail = request.POST['url_thumbnail']
        published_date_str = request.POST['published_date']
        print(published_date_str)
        published_date = parse(published_date_str)
        prev_path = request.POST['path']

        exist_bookmark_list = request.user.bookmarkvideo_set.filter(
            video__youtube_id=youtube_id)
        if exist_bookmark_list:
            exist_bookmark_list.delete()
        else:
            get_or_create_video_and_add_bookmark()
        return redirect(prev_path)


@login_required
def bookmark_list(request):
    # .all() 하면 데이터베이스에 계속 쿼리를 날리므로,
    # select_related()를 해주면 속도상 이점이 있다.
    bookmarks = request.user.bookmarkvideo_set.select_related('video')

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'video/bookmark_list.html', context)
