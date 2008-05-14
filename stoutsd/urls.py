from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'stoutsd.stout.views.home'),
)
