from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context_dict = {'boldmessage': "I am bold text from the context"}
    return render(request, 'rangoapp/index.html', context_dict)


def about(request):
    return render(request, 'rangoapp/about.html')
