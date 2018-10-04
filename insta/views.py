from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    images=Post.objects.all()
    return render(request, 'index.html',{'images':images,})