# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django.shortcuts import render_to_response
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory, SoupOfTheDay

def home(request):
    sotd = SoupOfTheDay.today()
    return render_to_response('home.html', dict(
            soup=sotd))

def menu(request):
    col1 = [MenuCategory.get_by_key_name("starters"),
            MenuCategory.get_by_key_name("soups"),
            MenuCategory.get_by_key_name("salads")]
    col2 = [MenuCategory.get_by_key_name("sandwiches"),
            MenuCategory.get_by_key_name("pub-grub")]
    col3 = [MenuCategory.get_by_key_name("main-course"),
            MenuCategory.get_by_key_name("sides"),
            MenuCategory.get_by_key_name("desserts")]
    return render_to_response('menu.html', dict(
            column_1=col1, column_2=col2, column_3=col3))
