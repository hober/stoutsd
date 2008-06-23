# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django import newforms as forms
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory, MenuItem

class MenuItemForm(forms.Form):
    category = forms.ChoiceField(
        choices=[(c.key(), c.name) for c in MenuCategory.all()],
        required=True)
    name = forms.CharField(required=True)
    price = forms.CharField(required=True)
    description = forms.CharField()
    display_on_menu = forms.BooleanField()

    def clean_name(self):
        name = self.clean_data.get('name', '')
        items = db.GqlQuery("SELECT * FROM MenuItem WHERE name = :1", name)
        if items.count() > 0:
            raise forms.ValidationError("Menu item already exists!")
        return name

class MenuCategoryForm(forms.Form):
    key = forms.CharField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)

class SoupOfTheDayForm(forms.Form):
    MenuItem.all()
    soup_choices = MenuItem.soup_choices()
    monday = forms.ChoiceField(required=True, choices=soup_choices)
    tuesday = forms.ChoiceField(required=True, choices=soup_choices)
    wednesday = forms.ChoiceField(required=True, choices=soup_choices)
    thursday = forms.ChoiceField(required=True, choices=soup_choices)
    friday = forms.ChoiceField(required=True, choices=soup_choices)
    saturday = forms.ChoiceField(required=True, choices=soup_choices)
    sunday = forms.ChoiceField(required=True, choices=soup_choices)
