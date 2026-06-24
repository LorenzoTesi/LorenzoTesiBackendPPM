from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def homePageView(request):
    return HttpResponse("Benvenuto nel Gestore di Eventi!")