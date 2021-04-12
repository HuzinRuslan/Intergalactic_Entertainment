from django.contrib.auth import get_user_model
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
        verbose_name = 'категория публикации'
        verbose_name_plural = 'категории публикаций'


class Publication(models.Model):
    category = models.ForeignKey(PublicationCategory, on_delete=models.CASCADE,
                                 verbose_name='категория публикации')
    user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                             verbose_name='автор публикации')
    name = models.CharField('имя публикации', max_length=128)
    image = models.ImageField(upload_to='publications_images', blank=True)
    short_desc = models.CharField('краткое описание публикации', max_length=64, blank=True)
    text = models.TextField('текст публикации', blank=True)
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    is_active = models.BooleanField(db_index=True, default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'

    def get_like_count(self):
        likes = len(Likes.objects.filter(publication_id=self.id, status=True))
        return likes

    def get_comment_count(self):
        comments = len(Comments.objects.filter(publication=self.id))
        return comments

    def is_liked(self, user):
        print(self.id)
        try:
            Likes.objects.get(sender_id=user, publication_id=self.id, status=True)
            print(user)
            return True
        except:
            print(user, 'da')
            return False


class Comments(models.Model):
    publication = models.ForeignKey(Publication, verbose_name='публикация',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(verbose_name='комментарий', blank=False)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Likes(models.Model):
    user_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                                  related_name='sender', default=0)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
    is_read = models.BooleanField(default=0)
