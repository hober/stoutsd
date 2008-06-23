# Copyright (C) 2008 Stout Public House. All Rights Reserved

import calendar
import os

import yaml

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from google.appengine.api import users
from google.appengine.ext import db

from stoutsd.stout.models import MenuItem, MenuCategory, SoupOfTheDay
from stoutsd.stout.admin.forms import MenuItemForm, MenuCategoryForm, \
    SoupOfTheDayForm

ADMINS=['hober0@gmail.com']
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

@adminonly('/admin/init')
def init (request):
    """"""
    pass

@adminonly('/admin')
def dashboard(request):
    return render_admin_template('admin/dashboard.html', dict())

@adminonly('/admin/load-fixtures')
def load_fixtures(request):
    fixtures = yaml.load(open(os.path.dirname(__file__) + '/../../fixtures.yaml', 'r'))

    menu_categories = fixtures['MenuCategory']
    menu_items = fixtures['MenuItem']

    categories_by_key = dict()

    for category in menu_categories:
        key = category['key']
        name = category.get('name', None)
        description = category.get('description', None)
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
        item = MenuItem(category=category, name=name, price=price, description=description,
                        show_on_menu=True)
        item.put()
        items.append(item)

    return render_admin_template('admin/fixtures.html', dict(
            menu_items=items,
            menu_categories=categories_by_key.values()))

@adminonly('/admin/menu')
def menu(request):
    return render_admin_template('admin/menu/dashboard.html', dict())

@adminonly('/admin/menu/categories')
def menu_categories(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            cat = MenuCategory(key_name=form.clean_data['key'],
                               name=form.clean_data['name'],
                               description=form.clean_data['description'])
            cat.put()
    else:
        form=MenuCategoryForm()

    categories = db.GqlQuery("SELECT * FROM MenuCategory")

    return render_admin_template('admin/menu/categories.html', dict(
            new_category_form=form,
            categories=categories))

@adminonly('/admin/menu/items')
def menu_items(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            cat_name = form.clean_data['category']

            cats = db.GqlQuery("SELECT * FROM MenuCategory WHERE name = :1", cat_name)

            item = MenuItem(category=cats[0],
                            name=form.clean_data['name'],
                            price=form.clean_data['price'],
                            description=form.clean_data['description'])
            item.put()
    else:
        form=MenuItemForm()

    items = db.GqlQuery("SELECT * FROM MenuItem")

    return render_admin_template('admin/menu/items.html', dict(
            items=items,
            new_item_form=form))

@adminonly('/admin/menu/soups')
def soup_of_the_day(request):
    if request.method == 'POST':
        form = SoupOfTheDayForm(request.POST)
        if form.is_valid():
            for day in xrange(len(calendar.day_name)):
                name = calendar.day_name[day]
                soup = MenuItem.get(form.clean_data[name.lower()])
                SoupOfTheDay.set_day(day, soup)
    else:
        form=SoupOfTheDayForm()

    return render_admin_template('admin/menu/soups.html', dict(
            soup_of_the_day_form=form))
