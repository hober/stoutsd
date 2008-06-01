from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^admin/menu/categories?$', 'stoutsd.stout.views.menu_category_admin'),
    (r'^admin/menu/items?$', 'stoutsd.stout.views.menu_item_admin'),
    (r'^admin/menu/?$', 'stoutsd.stout.views.menu_admin'),
    (r'^admin/?$', 'stoutsd.stout.views.admin'),
    (r'^$', 'stoutsd.stout.views.home'),
)
