# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory, SoupOfTheDay, Post, \
    Event, Game, AtomEntry, AtomFeed

def home(request):
    sotd = SoupOfTheDay.today()
    posts = Post.recent(5)
    events = Event.upcoming(5)
    games = Game.today()
    return render_to_response('home.html', dict(
            posts=posts, events=events, soup=sotd, games=games))

def feed(request):
    sotd = SoupOfTheDay.today()
    posts = Post.recent(5)
    events = Event.upcoming(5)
    feedobj = AtomFeed()
    entries = [AtomEntry(p) for p in posts] + [AtomEntry(e) for e in events]
    return HttpResponse(loader.render_to_string('feed.atom', dict(
            feed=feedobj, entries=entries)), mimetype="application/atom+xml")

def archives(request):
    posts = Post.all()
    return render_to_response('archives.html', dict(
            posts=posts))

def calendar(request):
    events = Event.upcoming(5)
    return render_to_response('calendar.html', dict(
            events=events))

def post(request, slug=None):
    post = None
    if slug is not None:
        post = Post.gql("WHERE slug = :1", slug).get()
    return render_to_response('post.html', dict(
            post=post))

def menu(request):
    col1 = [MenuCategory.get_by_key_name("starters"),
            MenuCategory.get_by_key_name("soups"),
            MenuCategory.get_by_key_name("salads")]
    col2 = [MenuCategory.get_by_key_name("sandwiches"),
            MenuCategory.get_by_key_name("pub-grub")]
    col3 = [MenuCategory.get_by_key_name("main-course"),
            # Anytime Breakfast
            MenuCategory.get("aghzdG91dHNkMnITCxIMTWVudUNhdGVnb3J5GJEcDA"),
            MenuCategory.get_by_key_name("sides"),
            MenuCategory.get_by_key_name("desserts")]
    return render_to_response('menu.html', dict(
            column_1=col1, column_2=col2, column_3=col3))
