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

class MenuItem(db.Model):
    category = db.ReferenceProperty(MenuCategory)
    name = db.StringProperty(multiline=False)
    price = db.StringProperty(multiline=False)
    description = db.StringProperty(multiline=False)
