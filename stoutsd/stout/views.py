# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.ext import db
from stoutsd.stout.models import Post

def home(request):
    Post.get_or_insert('hello', title="Hello, world", content="""
This is a test of the emergency broadcast system.

This is only a test.
""", published=db.DateTimeProperty.now())
    return render_to_response('home.html', dict(posts=Post.all()))
