from django.shortcuts import render


def main(request):
    content = {
        'title': 'главная',
    }
    return render(request, 'mainapp/index.html', content)
