# 소개
구현한 주요 기능은 다음과 같다.

1. 검색한 동영상 정보를 데이터베이스에 저장
2. Custom User 모델 생성
3. 검색한 동영상을 데이터베이스에 저장하지 않고 결과를 바로 출력하도록 변경
4. 검색을 POST요청으로 처리하던 것을 GET 요청으로 처리하게 변경
5. 검색 결과에 pageToken을 이용해, 이전/다음 페이지 기능 추가
6. 북마크 기능 추가 (북마크한 동영상만 데이터베이스에 저장)
7. 북마크 목록을 볼 수 있는 페이지 추가
8. 사용자별로 북마크를 구분하도록 구조 변경
9. 검색 결과에 북마크 추가/제거 버튼 추가


# 프로젝트 관리

```shell
.
├── django_app
│   ├── manage.py
│   └── youtube
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
└── requirements.txt

```

## Requirements
- Python (3.4.3)
- Django (1.10.5)
- google-api-python-client (1.6.2)
- requests (2.13.0)
- python-dateutil (2.6.0)

## Installation
```shell
$ pip install -r 'requierements.txt'
```