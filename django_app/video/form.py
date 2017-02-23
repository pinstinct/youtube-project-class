from django import forms

from video.models import Video


class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = (
            'bookmark',
        )
