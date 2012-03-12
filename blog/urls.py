from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('blog.views',
    (r'^$', 'index'),
    (r'^category/(?P<category_slug>[-_a-z]+)$', 'category'),
    (r'^(?P<article_slug>[-\w]+)$', 'show' ),
)
