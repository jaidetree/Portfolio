from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('associates.views',
    (r'^$', 'index'),
    (r'^(?P<name_slug>[-\w]+)$', 'show'),
)
