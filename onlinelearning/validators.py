from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_youtube(value):
    """Проверяем, что ссылка ведет на youtube.com"""
    if value:
        parsed_url = urlparse(value)
        if parsed_url.netloc not in ["youtube.com", "www.youtube.com"]:
            raise ValidationError("Разрешены только ссылки на youtube.com")
