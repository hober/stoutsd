# Copyright (C) 2008 Stout Public House. All Rights Reserved

import calendar, datetime

from google.appengine.ext import db

class EntryMixin:
    slug = db.StringProperty(multiline=False) # ?
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True, auto_now=True)

class Event(db.Model, EntryMixin):
    dtstart = db.DateTimeProperty()
    dtend = db.DateTimeProperty()

class Post(db.Model, EntryMixin):
    pass

MENU_CATEGORIES=["starter", "soup", "salad", "sandwich", "pub-fare",
                 "entree", "side", "dessert"]

class MenuCategory(db.Model):
    name = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)

    def items(self):
        return MenuItem.gql("WHERE show_on_menu = :1 AND category = :2", True, self)

class MenuItem(db.Model):
    category = db.ReferenceProperty(MenuCategory)
    name = db.StringProperty(multiline=False)
    price = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)
    show_on_menu = db.BooleanProperty()

    @staticmethod
    def soup_choices():
        soup_category = MenuCategory.get_by_key_name("soups")
        soups = MenuItem.gql("WHERE category = :1", soup_category)
        return [(soup.key(), soup.name) for soup in soups]

class SoupOfTheDay(db.Model):
    dayofweek = db.IntegerProperty(required=True)
    soup = db.ReferenceProperty(MenuItem, required=True)

    @staticmethod
    def set_day(day, soup):
        key = calendar.day_name[day].lower()
        try:
            sotd = SoupOfTheDay.get(key)
            sotd.dayofweek=day
            sotd.soup = soup
        except:
           sotd = SoupOfTheDay(key_name=key, dayofweek=day, soup=soup)
        sotd.put()

    @staticmethod
    def today():
        day = datetime.date.today().weekday()
        sotd = SoupOfTheDay.gql('WHERE dayofweek = :1', day)
        return sotd.get().soup
