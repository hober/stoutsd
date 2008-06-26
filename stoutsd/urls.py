# Copyright (C) 2008 Stout Public House. All Rights Reserved

from django.conf.urls.defaults import patterns

# Administrative interface
urlpatterns = patterns('stoutsd.stout.admin.views',
    (r'^admin/menu/categories/new/$', 'edit_menu_category'),
    (r'^admin/menu/categories/delete/(?P<key>.+)/$', 'delete_menu_category'),
    (r'^admin/menu/categories/edit/(?P<key>.+)/$', 'edit_menu_category'),
    (r'^admin/menu/categories/$', 'list_menu_categories'),

    (r'^admin/menu/items/new/$', 'edit_menu_item'),
    (r'^admin/menu/items/delete/(?P<key>.+)/$', 'delete_menu_item'),
    (r'^admin/menu/items/edit/(?P<key>.+)/$', 'edit_menu_item'),
    (r'^admin/menu/items/$', 'list_menu_items'),

    (r'^admin/menu/soups/$', 'soup_of_the_day'),
    (r'^admin/menu/$', 'menu'),

    (r'^admin/posts/new/$', 'edit_post'),
    (r'^admin/posts/delete/(?P<key>.+)/$', 'delete_post'),
    (r'^admin/posts/edit/(?P<key>.+)/$', 'edit_post'),
    (r'^admin/posts/$', 'list_posts'),

    (r'^admin/events/new/$', 'edit_event'),
    (r'^admin/events/delete/(?P<key>.+)/$', 'delete_event'),
    (r'^admin/events/edit/(?P<key>.+)/$', 'edit_event'),
    (r'^admin/events/$', 'list_events'),

    (r'^admin/games/new/$', 'edit_game'),
    (r'^admin/games/delete/(?P<key>.+)/$', 'delete_game'),
    (r'^admin/games/edit/(?P<key>.+)/$', 'edit_game'),
    (r'^admin/games/$', 'list_games'),

    (r'^admin/load-fixtures/$', 'load_fixtures'),
    (r'^admin/$', 'dashboard'),
)

# Public-facing pages
urlpatterns += patterns('stoutsd.stout.views',
    (r'^menu/$', 'menu'),
    (r'^\d+/\d+/(?P<slug>.+)/$', 'post'),
    (r'^posts/$', 'archives'),
    (r'^calendar/$', 'calendar'),
    (r'^feed/$', 'feed'),
    (r'^$', 'home'),
)
