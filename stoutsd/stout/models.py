from google.appengine.ext import db

# class Photo(db.Model):
#     pass

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
