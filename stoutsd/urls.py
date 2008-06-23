# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django.conf.urls.defaults import patterns

# Administrative interface
urlpatterns = patterns('stoutsd.stout.admin.views',
    (r'^admin/menu/categories/?$', 'menu_categories'),
    (r'^admin/menu/items/?$', 'menu_items'),
    (r'^admin/menu/soups/?$', 'soup_of_the_day'),
    (r'^admin/menu/?$', 'menu'),
    (r'^admin/load-fixtures/?$', 'load_fixtures'),
    (r'^admin/?$', 'dashboard'),
)

# Public-facing pages
urlpatterns += patterns('stoutsd.stout.views',
    (r'^menu/?$', 'menu'),
    (r'^$', 'home'),
)
