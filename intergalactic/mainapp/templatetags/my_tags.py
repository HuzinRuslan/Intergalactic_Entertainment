from django import template
from django.conf import settings
import re

register = template.Library()


def media_folder_publications(string):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    publications_images/product1.jpg --> /media/publications_images/product1.jpg
    """
    if not string:
        string = 'publications_images/default.png'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_publications', media_folder_publications)


@register.filter(name='is_liked')
def is_liked(publication, pk):
    return publication.is_liked(pk)


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'

    if bool(re.match('https', str(string))):
        return f'{string}'

    return f'{settings.MEDIA_URL}{string}'
