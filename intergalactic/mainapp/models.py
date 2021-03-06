from django.contrib.auth import get_user_model
from django.db import models
from authapp.models import IntergalacticUser
from ckeditor_uploader.fields import RichTextUploadingField


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
                                 verbose_name='категория')
    user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                             verbose_name='автор')
    name = models.CharField('заголовок', max_length=128)
    image = models.ImageField(upload_to='publications_images', blank=True,
                              verbose_name='главное изображение')
    short_desc = models.CharField('краткое описание', max_length=64,
                                  blank=True)
    text = RichTextUploadingField(blank=True, default='',
                                  verbose_name='контент')
    created = models.DateTimeField(verbose_name='создана', auto_now_add=True)
    is_active = models.BooleanField(db_index=True, default=True)
    on_moderator_check = models.BooleanField(db_index=True, default=False)
    moderator_refuse = RichTextUploadingField(blank=True, default='',
                                              verbose_name='комментарий')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'

    def get_like_count(self):
        likes = len(Likes.objects.filter(publication_id=self.id, status=True))
        return likes

    def get_dislike_count(self):
        dislikes = len(
            Dislikes.objects.filter(publication_id=self.id, status=True))
        return dislikes

    def get_comment_count(self):
        comments = len(Comments.objects.filter(publication=self.id))
        return comments

    def is_liked(self, user):
        try:
            Likes.objects.get(sender_id=user, publication_id=self.id,
                              status=True)
            return True
        except:
            return False

    def is_disliked(self, user):
        try:
            Dislikes.objects.get(sender_id=user, publication_id=self.id,
                                 status=True)
            return True
        except:
            return False

    def get_short_text(self):

        if len(self.text) > 1000:
            self.text = self.text[:350] + '...'
        return self.text

    def get_is_active(self):
        if self.on_moderator_check == True:
            return "На модерации"
        if self.is_active:
            return "Активна"
        else:
            return "Не активна"


class Comments(models.Model):
    publication = models.ForeignKey(Publication, verbose_name='публикация',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='отправитель')
    description = models.TextField(verbose_name='комментарий', blank=False)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    is_read = models.BooleanField(default=0)
    receiver = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                                 related_name='comments_sender', default=0,
                                 verbose_name='автор_публикации')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class ToComments(models.Model):
    comment = models.ForeignKey(Comments, verbose_name='коммент',
                                on_delete=models.CASCADE)
    to_user = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                                verbose_name='кого комментируем', default=0)
    for_comment = models.ForeignKey(Comments, on_delete=models.CASCADE,
                                    verbose_name='что комментируем', default=0,
                                    related_name='for_comment')

    class Meta:
        verbose_name = 'кому комментарий'
        verbose_name_plural = 'кому комментарии'


class Likes(models.Model):
    user_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                                  related_name='sender', default=0)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
    is_read = models.BooleanField(default=0)

    def change_status(self):
        changed = False
        if self.status:
            self.status = False
        else:
            try:
                dislike = Dislikes.objects.get(sender_id=self.sender_id,
                                               publication_id=self.publication_id)
                if dislike.status:
                    dislike.status = False
                    dislike.save()
                    changed = True
            except:
                pass
            self.status = True
        self.save()
        return changed

    @staticmethod
    def create(user, sender, publication):
        Likes.objects.create(user_id=user, sender_id=sender,
                             publication_id=publication, status=0)
        like = Likes.objects.get(sender_id=sender, publication_id=publication)
        return like.change_status()


class Dislikes(models.Model):
    user_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                                  related_name='dislike_sender', default=0)
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
    is_read = models.BooleanField(default=0)

    def change_status(self):
        changed = False
        if self.status:
            self.status = False
        else:
            try:
                like = Likes.objects.get(sender_id=self.sender_id,
                                         publication_id=self.publication_id)
                if like.status:
                    like.status = False
                    like.save()
                    changed = True
            except:
                pass
            self.status = True
        self.save()
        return changed

    @staticmethod
    def create(user, sender, publication):
        Dislikes.objects.create(user_id=user, sender_id=sender,
                                publication_id=publication, status=0)
        dislike = Dislikes.objects.get(sender_id=sender,
                                       publication_id=publication)
        return dislike.change_status()


# Таблица для подсчета количества просмотров статей
class ViewCounter(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


class ArticleRatings(models.Model):
    publication = models.ForeignKey(Publication, verbose_name='публикация',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='голосующий пользователь')
    rating = models.IntegerField(default=0, blank=True, verbose_name='рейтинг')

    @staticmethod
    def article_ratings(pk):
        return ArticleRatings.objects.filter(publication_id=pk)

    @staticmethod
    def average_pub_rating(pk):
        average_pub_rating = 0
        article_ratings = ArticleRatings.article_ratings(pk)
        for article_rating in article_ratings:
            average_pub_rating += article_rating.rating
        if len(article_ratings):
            average_pub_rating = (average_pub_rating / len(article_ratings))
        return round(average_pub_rating, 2)

    class Meta:
        verbose_name = 'рейтинг статьи'
        verbose_name_plural = 'рейтинги статей'


class UserRatings(models.Model):
    author = models.ForeignKey(IntergalacticUser, on_delete=models.CASCADE,
                               verbose_name='автор')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='голосующий пользователь',
                             related_name='voting_user', default=0)
    rating = models.IntegerField(default=0, blank=True, verbose_name='рейтинг')

    @staticmethod
    def average_author_rating(pk):
        average_author_rating = 0
        author_ratings = UserRatings.objects.filter(author_id=pk)
        aut_rat_quantity = len(author_ratings)
        if aut_rat_quantity:
            for author_rating in author_ratings:
                average_author_rating += author_rating.rating
            average_author_rating = (average_author_rating / aut_rat_quantity)

        average_article_rating = 0
        article_ratings = ArticleRatings.objects.filter(
            publication__user_id=pk)
        art_rat_quantity = len(article_ratings)
        if art_rat_quantity:
            for article_rating in article_ratings:
                average_article_rating += article_rating.rating
            average_article_rating = (
                    average_article_rating / art_rat_quantity)

        return round(((average_author_rating + average_article_rating) / 2), 2)

    class Meta:
        verbose_name = 'рейтинг автора'
        verbose_name_plural = 'рейтинги авторов'
