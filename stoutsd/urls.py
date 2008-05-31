from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^admin$', 'stoutsd.stout.views.admin'),
    (r'^$', 'stoutsd.stout.views.home'),
)
