from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'stoutsd.stout.views.home'),
)
