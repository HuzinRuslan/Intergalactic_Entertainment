from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from mainapp.models import Publication, PublicationCategory, Likes, Comments
from django.shortcuts import render, redirect
from django.http import HttpResponse
from authapp.models import IntergalacticUser
from notifications.signals import notify


def get_notifications(user):
    return Likes.objects.filter(user_id=user.id, is_read=False)


def get_comments(pk):
    return Comments.objects.filter(publication=pk)


def main(request):
    categories = PublicationCategory.objects.filter(is_active=True)
    publication_list = Publication.objects.filter(is_active=True,
                                                  category__is_active=True).order_by('-created')
    likes_list = get_notifications(request.user)

    content = {
        'categories': categories,
        'title': 'главная',
        'publication_list': publication_list,
        'likes': likes_list
    }
    return render(request, 'mainapp/index.html', content)


def publication_page(request, pk):
    categories = PublicationCategory.objects.filter(is_active=True)
    comments = get_comments(pk)
    likes = Likes.objects.all()
    context = {
        'page_title': 'Publication',
        'categories': categories,
        'publication': get_object_or_404(Publication, pk=pk),
        'comments': comments,
        'likes': likes
    }
    return render(request, 'mainapp/publication.html', context)


def category_page(request, pk):
    categories = PublicationCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            title = 'Все потоки'
            publications = Publication.objects.filter(is_active=True,
                                                      category__is_active=True).order_by('created')
        else:
            category = get_object_or_404(PublicationCategory, pk=pk)
            publications = Publication.objects.filter(category_id=pk, is_active=True,
                                                      category__is_active=True).order_by('created')
            title = category.name
        context = {
            'categories': categories,
            'title': title,
            'publications': publications
        }
        return render(request, 'mainapp/publication_category.html', context)


# def index(request):
#     try:
#         users = IntergalacticUser.objects.all()
#         print(request.user)
#         user = IntergalacticUser.objects.get(username=request.user)
#         return render(request, 'index.html', {'users': users, 'user': user})
#     except Exception as e:
#         print(e)
#         return HttpResponse("Please login from admin site for sending messages.")


def comment(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message != '':
            sender = IntergalacticUser.objects.get(username=request.user)
            publication = Publication.objects.get(id=request.POST.get('publication_id'))
            Comments.objects.create(publication=publication, user=sender, description=message)
            return redirect('main:main')
        else:
            raise ValidationError('is not an even number',)
    else:
        return HttpResponse("Invalid request")


def like(request, id, pk):
    publication = Publication.objects.get(id=id)
    sender = IntergalacticUser.objects.get(username=request.user)
    receiver = IntergalacticUser.objects.get(id=pk)
    try:
        liked = Likes.objects.get(sender_id=sender, publication_id=publication)
        if liked.status:
            liked.status = False
        else:
            liked.status = True
        liked.save()
    except:
        Likes.objects.create(user_id=receiver, sender_id=sender, publication_id=publication)
    return redirect('main:main')


def notification_read(request, pk):
    like = Likes.objects.get(id=pk)
    like.is_read = True
    like.save()

    return redirect('main:main')
