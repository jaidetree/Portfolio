from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('projects.views',
    (r'^$', 'index'),
    (r'^project/(?P<project_slug>[-a-z0-9]+)$', 'show'),
    (r'^resource/(?P<resource_slug>[-a-z0-9]+)$', 'resource'),
)
