from django.db import models
from authapp.models import IntergalacticUser


class PublicationCategory(models.Model):
    name = models.CharField(verbose_name='имя категории', max_length=120)
    desc = models.TextField(verbose_name='описание категории', blank=True)
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    is_active = models.BooleanField(db_index=True, default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория статьи'
        verbose_name_plural = 'категории статей'


class Publication(models.Model):
    category = models.ForeignKey(PublicationCategory, on_delete=models.CASCADE, verbose_name='категория продукта')
    user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE, verbose_name='автор статьи')
    name = models.CharField('имя статьи', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField('краткое описание статьи', max_length=64, blank=True)
    text = models.TextField('текст статьи', blank=True)
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    is_active = models.BooleanField(db_index=True, default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
