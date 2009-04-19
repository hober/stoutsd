# Copyright (C) 2008 Stout Public House. All Rights Reserved

import calendar
import csv
import datetime
import logging
import os

import yaml

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from google.appengine.api import users
from google.appengine.ext import db

from stoutsd.stout.models import MenuItem, MenuCategory, SoupOfTheDay, \
    Post, Event, Game
from stoutsd.stout.admin.forms import MenuItemForm, MenuCategoryForm, \
    SoupOfTheDayForm, PostForm, EventForm, GameForm

from stoutsd.utils import eastern_time

ADMINS=['hober0@gmail.com',
        'mark@stoutsd.com',
        'dave@stoutsd.com',
        'ted@stoutsd.com']
def adminonly(url):
    def _dec(view_func):
        def _checklogin(request, *args, **kwargs):
            user = users.get_current_user()
            if user and user.email() in ADMINS:
                return view_func(request, *args, **kwargs)
            elif user:
                return HttpResponseRedirect(users.create_logout_url(url))
            return HttpResponseRedirect(users.create_login_url(url))
        return _checklogin
    return _dec

def render_admin_template(tmpl, context):
    user = users.get_current_user()
    context['nickname'] = user.nickname()
    context['logout'] = users.create_logout_url("/")
    return render_to_response(tmpl, context)

@adminonly('/admin/')
def dashboard(request):
    return render_admin_template('admin/dashboard.html', dict())

@adminonly('/admin/load-nhl/')
def load_nhl(request):
    """Populate the data store with an initial set of games."""
    games = csv.reader(open(os.path.dirname(__file__) + '/../../nhl.csv', 'r'))
    gs = []
    for game in games:
        year = int(game[0])
        month = int(game[1])
        day = int(game[2])
        hour = int(game[3])
        minute = int(game[4])
        second = int(game[5])
        # dst = int(game[6])
        team1 = game[7]
        team2 = game[8]
        tzinfo = eastern_time
        dtstart = datetime.datetime(year, month, day, hour, minute, second, 0, tzinfo)
        g = Game(sport='NHL', team1=team1, team2=team2, dtstart=dtstart)
        g.put()
        gs.append(g)

    return render_admin_template('admin/games.html', dict(games=gs))

@adminonly('/admin/load-fixtures/')
def load_fixtures(request):
    """Populate the data store with an initial set of data."""
    fixtures = yaml.load(open(os.path.dirname(__file__) + '/../../fixtures.yaml', 'r'))

    menu_categories = fixtures['MenuCategory']
    menu_items = fixtures['MenuItem']

    categories_by_key = dict()

    for category in menu_categories:
        key = category['key']
        name = category.get('name', '')
        description = category.get('description', '')
        cat = MenuCategory(key_name=key, name=name,
                           description=description)
        cat.put()
        categories_by_key[key] = cat

    items = []
    for item in menu_items:
        category = categories_by_key[item['category']]
        name = item.get('name', None)
        price = str(item.get('price', None))
        description = item.get('description', None)
        show_on_menu = item.get('show_on_menu', False)
        item = MenuItem(category=category, name=name, price=price, description=description,
                        show_on_menu=show_on_menu)
        item.put()
        items.append(item)

    return render_admin_template('admin/fixtures.html', dict(
            menu_items=items,
            menu_categories=categories_by_key.values()))

@adminonly('/admin/menu/')
def menu(request):
    return render_admin_template('admin/menu/dashboard.html', dict())

@adminonly('/admin/menu/categories/')
def list_menu_categories(request):
    categories = db.GqlQuery("SELECT * FROM MenuCategory")
    return render_admin_template('admin/menu/categories/list.html', dict(
            categories=categories))

@adminonly('/admin/menu/categories/')
def edit_menu_category(request, key=None):
    category = None
    if key is not None:
        category = MenuCategory.get(key)
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            cat = MenuCategory.from_form(form)
            cat.put()
            return HttpResponseRedirect('/admin/menu/categories/')
    elif category:
        form = MenuCategoryForm({
                'name': category.name,
                'description': category.description,
                # Hidden
                'key': category.key()})
    else:
        form=MenuCategoryForm()
    return render_admin_template('admin/menu/categories/edit.html', dict(
            category=category, category_form=form))

@adminonly('/admin/menu/categories/delete/')
def delete_menu_category(request, key=None):
    category = None
    if key is not None:
        category = MenuCategory.get(key)
    if key and request.method == 'POST':
        category.delete()
    return HttpResponseRedirect('/admin/menu/categories/')

@adminonly('/admin/menu/items/')
def list_menu_items(request):
    items = db.GqlQuery("SELECT * FROM MenuItem")
    return render_admin_template('admin/menu/items/list.html', dict(
            items=items))

@adminonly('/admin/menu/items/')
def edit_menu_item(request, key=None):
    item = None
    if key is not None:
        item = MenuItem.get(key)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = MenuItem.from_form(form, key)
            item.put()
            return HttpResponseRedirect('/admin/menu/items/')
    elif item:
        form = MenuItemForm({
    		'category': item.category.key(),
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'show_on_menu': item.show_on_menu,
                # Hidden
                'key': item.key()})
    else:
        form=MenuItemForm()
    return render_admin_template('admin/menu/items/edit.html', dict(
            item=item, item_form=form))

@adminonly('/admin/menu/items/delete/')
def delete_menu_item(request, key=None):
    item = None
    if key is not None:
        item = MenuItem.get(key)
    if key and request.method == 'POST':
        item.delete()
    return HttpResponseRedirect('/admin/menu/items/')


# Posts


@adminonly('/admin/posts/')
def list_posts(request):
    posts = db.GqlQuery("SELECT * FROM Post")
    return render_admin_template('admin/posts/list.html', dict(
            posts=posts))

@adminonly('/admin/posts/edit/')
def edit_post(request, key=None):
    post = None
    if key is not None:
        post = Post.get(key)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.from_form(form)
            post.put()
            return HttpResponseRedirect('/admin/posts/')
    elif post:
        form = PostForm({'title': post.title,
                         'content': post.content,
                         'publish': (post.published is not None),
                         # Hidden
                         'key': post.key(),
                         'slug': post.slug,
                         'published': post.published,
                         'updated': post.updated})
    else:
        form = PostForm()

    return render_admin_template('admin/posts/edit.html', dict(
            post=post, post_form=form))

@adminonly('/admin/posts/delete/')
def delete_post(request, key=None):
    post = None
    if key is not None:
        post = Post.get(key)
    if key and request.method == 'POST':
        post.delete()
    return HttpResponseRedirect('/admin/posts/')

# Events

@adminonly('/admin/events/')
def list_events(request):
    events = db.GqlQuery("SELECT * FROM Event")
    return render_admin_template('admin/events/list.html', dict(
            events=events))

@adminonly('/admin/events/edit/')
def edit_event(request, key=None):
    event = None
    if key is not None:
        event = Event.get(key)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = Event.from_form(form)
            event.put()
            return HttpResponseRedirect('/admin/events/')
    elif event:
        form = EventForm({'title': event.title,
                         'content': event.content,
                         'publish': (event.published is not None),
                         # Hidden
                         'key': event.key(),
                         'slug': event.slug,
                         'published': event.published,
                         'updated': event.updated})
    else:
        form = EventForm()

    return render_admin_template('admin/events/edit.html', dict(
            event=event, event_form=form))

@adminonly('/admin/events/delete/')
def delete_event(request, key=None):
    event = None
    if key is not None:
        event = Event.get(key)
    if key and request.method == 'POST':
        event.delete()
    return HttpResponseRedirect('/admin/events/')

# Games

@adminonly('/admin/games/')
def list_games(request):
    games = db.GqlQuery("SELECT * FROM Game")
    return render_admin_template('admin/games/list.html', dict(
            games=games))

@adminonly('/admin/games/edit/')
def edit_game(request, key=None):
    game = None
    if key is not None:
        game = Game.get(key)
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game.from_form(form)
            game.put()
            return HttpResponseRedirect('/admin/games/')
    elif game:
        form = GameForm({'sport': game.sport,
                         'team1': game.team1,
                         'team2': game.team2,
                         'dtstart': game.dtstart})
    else:
        form = GameForm()

    return render_admin_template('admin/games/edit.html', dict(
            game=game, game_form=form))

@adminonly('/admin/games/delete/')
def delete_game(request, key=None):
    game = None
    if key is not None:
        game = Game.get(key)
    if key and request.method == 'POST':
        game.delete()
    return HttpResponseRedirect('/admin/games/')
