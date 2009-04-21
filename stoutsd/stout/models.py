# Copyright (C) 2008 Stout Public House. All Rights Reserved

import calendar
import datetime
import markdown

from django.template.defaultfilters import slugify

from google.appengine.ext import db

from stoutsd.utils import pacific_time

HUMAN_DT_FORMAT = "%B %d @ %H:%M"
HUMAN_DATE_FORMAT = "%B %d, %Y"
ATOM_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

SHORT_DATE_FORMAT = "%A %m/%d/%y"
SHORT_TIME_FORMAT = "%H:%M"

def date_format_property(field, format):
    def formatter (self):
        return field(self).strftime(format)
    return formatter

class Game(db.Model):
    sport = db.StringProperty(multiline=False)
    team1 = db.StringProperty(multiline=False)
    team2 = db.StringProperty(multiline=False)
    dtstart = db.DateTimeProperty()

    def date_human(self):
        return self.dtstart.replace(tzinfo=pacific_time).strftime(SHORT_DATE_FORMAT)

    def time_human(self):
        return self.dtstart.replace(tzinfo=pacific_time).strftime(SHORT_TIME_FORMAT)

    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        d = form.clean_data['start_date']
        t = form.clean_data['start_time']
        dt = datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, pacific_time)
        form.clean_data['dtstart'] = dt
        return Game(**form.clean_data)

    @staticmethod
    def today():
        today = datetime.date.today()
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return Game.gql("WHERE dtstart >= :1 AND dtstart < :2 ORDER BY dtstart ASC", today, tomorrow)

# Methods shared by Event and Post.
class EntryMixin:
    published_human = date_format_property(lambda self: self.published,
                                           HUMAN_DT_FORMAT)
    updated_human = date_format_property(lambda self: self.updated,
                                           HUMAN_DT_FORMAT)
    published_date = date_format_property(lambda self: self.published,
                                           HUMAN_DATE_FORMAT)

class Event(EntryMixin, db.Model):
    slug = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    content_rendered = db.TextProperty()
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True, auto_now=True)
    dtstart = db.DateTimeProperty()
    dtend = db.DateTimeProperty()
    all_day = db.BooleanProperty()

    # FIXME: should be 12pm &#8212; May 10th, 2008
    dtstart_human = date_format_property(lambda self: self.dtstart,
                                           HUMAN_DT_FORMAT)
    dtend_human = date_format_property(lambda self: self.dtend,
                                           HUMAN_DT_FORMAT)

    def url(self):
        return '/events/%04d/%02d/%s/' % (
            self.published.year, self.published.month, self.slug)

    @staticmethod
    def upcoming(limit=None):
        today = datetime.date.today()
        now = datetime.datetime(today.year, today.month, today.day,
                                0, 0, 0)
        if limit is not None:
            limit = " LIMIT %d" % limit
        else:
            limit = ""
        return Event.gql("WHERE dtstart >= :1 ORDER BY dtstart ASC%s" % limit, now)

    # I should really rethink the model<->form relationship.
    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        title = form.clean_data['title']
        content = form.clean_data['content']
        content_rendered = markdown.markdown(content)
        publish = form.clean_data['publish']

        d = form.clean_data['start_date']
        t = form.clean_data['start_time']
        dtstart = datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, pacific_time)
        d = form.clean_data['end_date']
        t = form.clean_data['end_time']
        dtend = datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, pacific_time)

        all_day = form.clean_data['all_day']
        # Existing objects only
        key = form.clean_data['key']
        # Create/modify the post
        updated = datetime.datetime.now()
        if key:
            existing = Event.get(key)
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
            return Event(slug=slugify(title), title=title, content=content,
                         content_rendered=content_rendered,
                         published=published, updated=updated,
                         dtstart=dtstart, dtend=dtend, all_day=all_day)

class Post(EntryMixin, db.Model):
    slug = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    content = db.TextProperty()
    content_rendered = db.TextProperty()
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now_add=True, auto_now=True)

    @staticmethod
    def recent(limit=None):
        if limit is not None:
            limit = " LIMIT %d" % limit
        else:
            limit = ""
        return Post.gql("ORDER BY updated%s" % limit)

    def url(self):
        return '/%04d/%02d/%s/' % (
            self.published.year, self.published.month, self.slug)

    # I should really rethink the model<->form relationship.
    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        title = form.clean_data['title']
        content = form.clean_data['content']
        content_rendered = markdown.markdown(content)
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
                        content_rendered=content_rendered,
                        published=published, updated=updated)

class MenuCategory(db.Model):
    name = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)

    def items(self):
        return MenuItem.gql("WHERE show_on_menu = :1 AND category = :2", True, self)

    @staticmethod
    def from_form(form):
        if not form.is_valid(): return None
        name = form.clean_data['name']
        description = form.clean_data['description']
        # Existing objects only
        key = form.clean_data['key']
        if key:
            existing = MenuCategory.get(key)
            existing.name = name
            existing.description = description
            return existing
        else:
            return MenuCategory(name=name, description=description)

class MenuItem(db.Model):
    category = db.ReferenceProperty(MenuCategory)
    name = db.StringProperty(multiline=False)
    price = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)
    show_on_menu = db.BooleanProperty(default=True)

    @staticmethod
    def from_form(form, key=None):
        if not form.is_valid(): return None
        name = form.clean_data['name']
        price = form.clean_data['price']
        description = form.clean_data['description']
        show_on_menu = form.clean_data['show_on_menu']
        # Existing objects only
        if key is None and 'key' in form.clean_data:
            key = form.clean_data['key']
        if key:
            existing = MenuItem.get(key)
            existing.name = name
            existing.price = price
            existing.description = description
            existing.show_on_menu = show_on_menu
            return existing
        else:
            return MenuItem(name=name, price=price, description=description,
                            show_on_menu=show_on_menu)

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

class AtomEntry:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def id(self):
        return "tag:stoutsd.com,%s:%s" % (
            self.wrapped.published.strftime("%Y-%m-%d"),
            self.wrapped.slug)

    def url(self):
        return self.wrapped.url()

    published = date_format_property(lambda self: self.wrapped.published,
                                     ATOM_DATE_FORMAT)
    updated = date_format_property(lambda self: self.wrapped.updated,
                                     ATOM_DATE_FORMAT)

    def title(self):
        return self.wrapped.title

    def content(self):
        return self.wrapped.content

    def is_event(self):
        return hasattr(self.wrapped, 'dtstart')

    def dtstart(self):
        if self.is_event():
            return self.wrapped.dtstart.strftime(HUMAN_DT_FORMAT)

class AtomFeed:
    def __init__(self):
        self.id = "tag:stoutsd.com,2008:feed"
        self.alternate = "http://stoutsd.com/"
        self.url = "http://stoutsd.com/feed/"
        self.title = "Stout Public House"
        self.entries = []

    def updated(self):
        # steal from most recently updated entry
        pass
