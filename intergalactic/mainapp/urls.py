from django.urls import path, include
from django.conf.urls import url
import notifications.urls
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('publication/<int:pk>', mainapp.publication_page, name='publication_page'),
    path('category/<int:pk>', mainapp.category_page, name='category'),
    path('comment/', mainapp.comment, name='comment'),
    path('like/<int:id>/<int:pk>', mainapp.like, name='like'),
    path('notification_read/<int:pk>', mainapp.notification_read, name='notification_read'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
