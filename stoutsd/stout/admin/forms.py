# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django import newforms as forms
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory, MenuItem

class RequiredFieldMixin:
    """Ensure required fields have the jquery.validate class applied"""
    def widget_attrs(self, widget):
        return {'class': 'required'}

class RequiredCharField(RequiredFieldMixin, forms.CharField):
    def __init__ (self, *args, **kwargs):
        kwargs['required'] = True
        forms.CharField.__init__(self, *args, **kwargs)

class RequiredChoiceField(RequiredFieldMixin, forms.ChoiceField):
    def __init__ (self, *args, **kwargs):
        kwargs['required'] = True
        forms.ChoiceField.__init__(self, *args, **kwargs)

class GameForm(forms.Form):
    sport = RequiredChoiceField(choices=[
            ("MLB","Baseball"),
            ("NHL","Hockey"),
            ("NBA","Basketball"),
            ("NFL","Football"),
            ("Soccer","Soccer")])
    team1 = RequiredCharField()
    team2 = RequiredCharField()
    dtstart = forms.DateTimeField(required=True)

class PostForm(forms.Form):
    title = RequiredCharField()
    content = RequiredCharField(widget=forms.Textarea)
    publish = forms.BooleanField(required=False)
    key = forms.CharField(required=False, widget=forms.HiddenInput)

class EventForm(forms.Form):
    title = RequiredCharField()
    content = RequiredCharField(widget=forms.Textarea)
    publish = forms.BooleanField(required=False)
    key = forms.CharField(required=False, widget=forms.HiddenInput)
    start = forms.DateTimeField(required=True)
    end = forms.DateTimeField(required=False)
    all_day = forms.BooleanField(required=False)

class MenuItemForm(forms.Form):
    category = RequiredChoiceField(
        choices=[(c.key(), c.name) for c in MenuCategory.all()])
    name = RequiredCharField()
    price = RequiredCharField()
    description = forms.CharField(required=False)
    display_on_menu = forms.BooleanField()

    def clean_name(self):
        name = self.clean_data.get('name', '')
        items = db.GqlQuery("SELECT * FROM MenuItem WHERE name = :1", name)
        if items.count() > 0:
            raise forms.ValidationError("Menu item already exists!")
        return name

class MenuCategoryForm(forms.Form):
    key = RequiredCharField()
    name = RequiredCharField()
    description = forms.CharField(required=False)

class SoupOfTheDayForm(forms.Form):
    MenuItem.all()
    soup_choices = MenuItem.soup_choices()
    # initial=that_days_dude
    monday = RequiredChoiceField(required=True, choices=soup_choices)
    tuesday = RequiredChoiceField(required=True, choices=soup_choices)
    wednesday = RequiredChoiceField(required=True, choices=soup_choices)
    thursday = RequiredChoiceField(required=True, choices=soup_choices)
    friday = RequiredChoiceField(required=True, choices=soup_choices)
    saturday = RequiredChoiceField(required=True, choices=soup_choices)
    sunday = RequiredChoiceField(required=True, choices=soup_choices)
