import re
from rest_framework import serializers

def validate_video_link(value):
    """
    Проверяет, что ссылка содержит youtube.com.
    Если ссылка есть, но не содержит youtube.com — вызывает ошибку.
    """
    # Если поле пустое, пропускаем
    if not value:
        return value

    # Если поле — просто ссылка, можно проверить напрямую:
    if isinstance(value, str):
        # Проверяем, что в ссылке есть youtube.com
        if "youtube.com" not in value:
            raise serializers.ValidationError("Допустимы только ссылки на youtube.com")
    else:
        # Если поле не строка — возможно, другое представление, просто пропускаем
        pass

    return value
