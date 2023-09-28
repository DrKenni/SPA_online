from rest_framework.serializers import ValidationError


class VideoURLValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, value) -> None:
        url = dict(value).get(self.field)
        if url is not None and 'youtube.com' not in url:
            raise ValidationError('Можно вставить только видео с YouTube.com')
