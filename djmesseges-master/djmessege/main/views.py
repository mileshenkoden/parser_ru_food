from django.shortcuts import render
from django.template.defaultfilters import title


def index(request):
    data = {
        'title': 'Головна сторінка',
        'values': ['123' ,"Some", "kok"]
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')
