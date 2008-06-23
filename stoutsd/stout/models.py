# Copyright (C) 2008 Stout Public House. All Rights Reserved

import calendar, datetime

from django.template.defaultfilters import slugify

from google.appengine.ext import db

# class Event(db.Model):
#     dtstart = db.DateTimeProperty()
#     dtend = db.DateTimeProperty()
#     slug = db.StringProperty(multiline=False) # ?
#     title = db.StringProperty(multiline=False)
#     content = db.TextProperty()
#     published = db.DateTimeProperty(auto_now_add=True)
#     updated = db.DateTimeProperty(auto_now_add=True, auto_now=True)

class Post(db.Model):
    slug = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True, auto_now=True)

    def link(self):
        return '/posts/%d/%d/%s/' % (self.published.year,
                                     self.published.month,
                                     self.slug())

    def published_human(self):
        return self.published.strftime("%B %d @ %H:%M")

    @staticmethod
    def recent():
        return Post.gql("ORDER BY updated LIMIT 5")

    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        title = form.clean_data['title']
        content = form.clean_data['content']
        publish = form.clean_data['publish']
        # Existing objects only
        key = form.clean_data['key']
        # Create/modify the post
        updated = datetime.datetime.now()
        if key:
            existing = Post.get(key)
            existing.title = title
            existing.content = content
            existing.updated = updated
            if publish:
                if not existing.published:
                    existing.published = updated
            else:
                existing.published = None
            return existing
        else:
            published = updated if publish else None
            return Post(slug=slugify(title), title=title, content=content,
                        published=published, updated=updated)

class MenuCategory(db.Model):
    name = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)

    def items(self):
        return MenuItem.gql("WHERE show_on_menu = :1 AND category = :2", True, self)

    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        return MenuCategory(key_name=form.clean_data['key'],
                            name=form.clean_data['name'],
                            description=form.clean_data['description'])

class MenuItem(db.Model):
    category = db.ReferenceProperty(MenuCategory)
    name = db.StringProperty(multiline=False)
    price = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)
    show_on_menu = db.BooleanProperty(default=True)

    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        cat_key = form.clean_data['category']
        cat = MenuCategory.get(cat_key)
        return MenuItem(category=cat,
                        name=form.clean_data['name'],
                        price=form.clean_data['price'],
                        description=form.clean_data['description'],
                        show_on_menu=form.clean_data['display_on_menu'])

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
        sotd = SoupOfTheDay.gql('WHERE dayofweek = :1', day).get()
        if sotd:
            return sotd.soup
        else:
            return None
