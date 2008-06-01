from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.ext import db
from stoutsd.stout.models import Post, MenuItem, MenuCategory
from forms import MenuItemForm, MenuCategoryForm

ADMINS=['hober0@gmail.com']
def adminonly(url):
    def _dec(view_func):
        def _checklogin(request, *args, **kwargs):
            user = users.get_current_user()
            if user and user.email() in ADMINS:
                return view_func(request, *args, **kwargs)
            elif user:
                return HttpResponseRedirect(users.create_logout_url(url))
            return HttpResponseRedirect(users.create_login_url(url))
        return _checklogin
    return _dec



def home(request):
    from google.appengine.ext import db
    Post.get_or_insert('hello', title="Hello, world", content="""
This is a test of the emergency broadcast system.

This is only a test.
""", published=db.DateTimeProperty.now())
    return render_to_response('home.html', dict(posts=Post.all()))

def render_admin_template(tmpl, context):
    user = users.get_current_user()
    context['nickname'] = user.nickname()
    context['logout'] = users.create_logout_url("/")
    return render_to_response(tmpl, context)

@adminonly('/admin')
def admin(request):
    return render_admin_template('admin/dashboard.html', dict())


@adminonly('/admin/menu')
def menu_admin(request):
    return render_admin_template('admin/menu/dashboard.html', dict())

@adminonly('/admin/menu/categories')
def menu_category_admin(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            cat = MenuCategory(name=form.clean_data['name'],
                               description=form.clean_data['description'])
            cat.put()
    else:
        form=MenuCategoryForm()

    categories = db.GqlQuery("SELECT * FROM MenuCategory")

    return render_admin_template('admin/menu/categories.html', dict(
            new_category_form=form,
            categories=categories))

@adminonly('/admin/menu/items')
def menu_item_admin(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            cat_name = form.clean_data['category']

            cats = db.GqlQuery("SELECT * FROM MenuCategory WHERE name = :1", cat_name)

            item = MenuItem(category=cats[0],
                            name=form.clean_data['name'],
                            price=form.clean_data['price'],
                            description=form.clean_data['description'])
            item.put()
    else:
        form=MenuItemForm()

    items = db.GqlQuery("SELECT * FROM MenuItem")

    return render_admin_template('admin/menu/items.html', dict(
            items=items,
            new_item_form=form))
