from django.conf.urls.defaults import patterns

urlpatterns = patterns('stoutsd.stout.admin.views',
    # Administrative interface
    (r'^admin/menu/categories?$', 'menu_categories'),
    (r'^admin/menu/items?$', 'menu_items'),
    (r'^admin/menu/?$', 'menu_dashboard'),
    (r'^admin/?$', 'dashboard'),
)

urlpatterns += patterns('stoutsd.stout.views',
    # Public-facing pages
    (r'^menu/?$', 'menu'),
    (r'^$', 'home'),
)
