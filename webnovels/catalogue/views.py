from django.shortcuts import render
from django.http import HttpResponse
from .models import novels,chapter

def index(request):
    return HttpResponse('Hello World')