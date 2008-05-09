from django.http import HttpResponse, HttpResponseRedirect
from stoutsd.stout import models
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html', {})
