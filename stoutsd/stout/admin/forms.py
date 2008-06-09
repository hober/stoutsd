from django import newforms as forms
from google.appengine.ext import db
from stoutsd.stout.models import MenuCategory

class MenuItemForm(forms.Form):
    category = forms.ChoiceField(
        choices=[(c.name, c.name) for c in MenuCategory.all()],
        required=True)
    name = forms.CharField(required=True)
    price = forms.CharField(required=True)
    description = forms.CharField()

    def clean_name(self):
        name = self.clean_data.get('name', '')
        items = db.GqlQuery("SELECT * FROM MenuItem WHERE name = :1", name)
        if items.count() > 0:
            raise forms.ValidationError("Menu item already exists!")
        return name

class MenuCategoryForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
