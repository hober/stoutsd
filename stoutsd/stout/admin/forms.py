# Copyright (C) 2008 Stout Public House. All Rights Reserved

import logging

from django import forms
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory, MenuItem

class RequiredFieldMixin:
    """Ensure required fields have the jquery.validate class applied"""
    def widget_attrs(self, widget):
        return {'class': 'required'}

class RequiredCharField(RequiredFieldMixin, forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['required'] = True
        forms.CharField.__init__(self, *args, **kwargs)

class RequiredChoiceField(RequiredFieldMixin, forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['required'] = True
        forms.ChoiceField.__init__(self, *args, **kwargs)

class DatePickerField(forms.DateField):
    def widget_attrs(self, widget):
        return {'class': 'pickme'}

class GameForm(forms.Form):
    sport = RequiredChoiceField(choices=[
            ("MLB","Baseball"),
            ("NHL","Hockey"),
            ("NBA","Basketball"),
            ("NFL","Football"),
            ("Soccer","Soccer")])
    team1 = RequiredCharField()
    team2 = RequiredCharField()
    start_date = DatePickerField(required=True)
    start_time = forms.TimeField(required=True)

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
    start_date = DatePickerField(required=True)
    start_time = forms.TimeField(required=True)
    end_date = DatePickerField(required=False)
    end_time = forms.TimeField(required=False)
    all_day = forms.BooleanField(required=False)

class MenuItemForm(forms.Form):
    category = RequiredChoiceField(
        choices=[(c.key(), c.name) for c in MenuCategory.all()])
    name = RequiredCharField()
    price = RequiredCharField()
    description = forms.CharField(required=False)
    show_on_menu = forms.BooleanField()

class MenuCategoryForm(forms.Form):
    key = forms.CharField(required=False, widget=forms.HiddenInput)
    name = RequiredCharField()
    description = forms.CharField(required=False)
    column = forms.ChoiceField(
        required=True, choices=[('1','1'),('2','2'),('3','3')])
    order = forms.IntegerField(required=True)

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
